#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市策略MCP工具服务器

提供MCP工具接口，支持：
- bull_market.extract_patterns - 提取牛市规律
- bull_market.detect_state - 检测牛市状态
- bull_market.generate_strategy - 生成策略
- bull_market.backtest - 执行回测
- bull_market.evolve - 递归进化
- bull_market.full_workflow - 完整工作流
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
import json

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger('BullMarketStrategyServer')

# 导入MCP SDK
try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
    MCP_SDK_AVAILABLE = True
except ImportError:
    logger.error("MCP SDK不可用，请安装: pip install mcp")
    logger.error(f"当前Python路径: {sys.executable}")
    # 检查是否是系统Python
    if 'venv' not in sys.executable and 'virtualenv' not in sys.executable:
        logger.error("⚠️  检测到使用系统Python，请使用venv中的Python:")
        venv_python = Path(__file__).parent.parent / "venv" / "bin" / "python3"
        if venv_python.exists():
            logger.error(f"  建议使用: {venv_python}")
    sys.exit(1)

# 创建服务器
server = Server("bull-market-strategy")


# ==================== 工具定义 ====================

@server.list_tools()
async def list_tools() -> List[Tool]:
    """列出所有可用工具"""
    return [
        Tool(
            name="bull_market.extract_patterns",
            description="提取牛市专属模式：从历史牛市高回报案例中提取规律模式（动量突破、板块轮动等）",
            inputSchema={
                "type": "object",
                "properties": {
                    "cases_csv_path": {
                        "type": "string",
                        "description": "高回报案例CSV文件路径（如果为None，将自动挖掘）"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "数据挖掘开始日期（YYYY-MM-DD）",
                        "default": "2024-09-01"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "数据挖掘结束日期（YYYY-MM-DD）",
                        "default": "2025-09-13"
                    },
                    "min_return_pct": {
                        "type": "number",
                        "description": "最低收益率（%）",
                        "default": 10.0
                    },
                    "n_clusters": {
                        "type": "integer",
                        "description": "聚类数量",
                        "default": 4
                    },
                    "output_json_path": {
                        "type": "string",
                        "description": "输出JSON文件路径",
                        "default": "data/bull_market_patterns.json"
                    }
                }
            }
        ),
        Tool(
            name="bull_market.detect_state",
            description="检测牛市状态：检测当前市场是否为牛市，并返回强度等级和概率",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "检测日期（YYYY-MM-DD，None表示今天）"
                    },
                    "benchmark": {
                        "type": "string",
                        "description": "基准指数",
                        "default": "000300.XSHG"
                    }
                }
            }
        ),
        Tool(
            name="bull_market.generate_strategy",
            description="生成混合策略：根据牛市强度生成策略代码（7因子+牛市模式）",
            inputSchema={
                "type": "object",
                "properties": {
                    "bull_strength": {
                        "type": "number",
                        "description": "牛市强度得分（0-100）",
                        "default": 70.0
                    },
                    "strategy_mode": {
                        "type": "string",
                        "description": "策略模式（BULL_AGGRESSIVE/BULL_MIXED/BASE_FACTOR）",
                        "enum": ["BULL_AGGRESSIVE", "BULL_MIXED", "BASE_FACTOR", "AUTO"]
                    },
                    "output_path": {
                        "type": "string",
                        "description": "策略代码输出路径（可选）"
                    }
                }
            }
        ),
        Tool(
            name="bull_market.backtest",
            description="执行BulletTrade回测：使用指定参数执行回测并返回标准化结果",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy_params": {
                        "type": "object",
                        "description": "策略参数字典"
                    },
                    "strategy_code": {
                        "type": "string",
                        "description": "策略代码（可选，如果不提供将根据params生成）"
                    },
                    "start_date": {
                        "type": "string",
                        "description": "回测开始日期（YYYY-MM-DD）",
                        "default": "2024-10-01"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "回测结束日期（YYYY-MM-DD）",
                        "default": "2024-12-31"
                    },
                    "initial_capital": {
                        "type": "number",
                        "description": "初始资金",
                        "default": 1000000.0
                    },
                    "backtest_id": {
                        "type": "string",
                        "description": "回测ID（可选）"
                    }
                },
                "required": ["strategy_params"]
            }
        ),
        Tool(
            name="bull_market.evolve",
            description="递归进化优化：使用遗传算法优化策略参数，目标月回报率30%",
            inputSchema={
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "回测开始日期（YYYY-MM-DD）",
                        "default": "2024-10-01"
                    },
                    "end_date": {
                        "type": "string",
                        "description": "回测结束日期（YYYY-MM-DD）",
                        "default": "2024-12-31"
                    },
                    "population_size": {
                        "type": "integer",
                        "description": "种群大小",
                        "default": 50
                    },
                    "generations": {
                        "type": "integer",
                        "description": "进化代数",
                        "default": 10
                    },
                    "target_monthly_return": {
                        "type": "number",
                        "description": "目标月回报率（小数，如0.30表示30%）",
                        "default": 0.30
                    },
                    "max_drawdown_limit": {
                        "type": "number",
                        "description": "最大回撤限制（负数，如-0.20表示-20%）",
                        "default": -0.20
                    },
                    "min_sharpe_ratio": {
                        "type": "number",
                        "description": "最小夏普比率",
                        "default": 2.0
                    },
                    "output_dir": {
                        "type": "string",
                        "description": "输出目录",
                        "default": "output/evolution"
                    }
                }
            }
        ),
        Tool(
            name="bull_market.full_workflow",
            description="完整工作流：执行端到端的完整工作流（检测市场→挖掘数据→提取模式→生成策略→回测→进化→归档）",
            inputSchema={
                "type": "object",
                "properties": {
                    "skip_mining": {
                        "type": "boolean",
                        "description": "是否跳过数据挖掘（使用已有数据）",
                        "default": False
                    },
                    "skip_evolution": {
                        "type": "boolean",
                        "description": "是否跳过进化优化（只执行一次回测）",
                        "default": False
                    },
                    "workflow_config": {
                        "type": "object",
                        "description": "工作流配置（可选，使用默认值）"
                    }
                }
            }
        ),
    ]


# ==================== 工具处理函数 ====================

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """处理工具调用"""
    try:
        if name == "bull_market.extract_patterns":
            result = await _handle_extract_patterns(arguments)
        elif name == "bull_market.detect_state":
            result = await _handle_detect_state(arguments)
        elif name == "bull_market.generate_strategy":
            result = await _handle_generate_strategy(arguments)
        elif name == "bull_market.backtest":
            result = await _handle_backtest(arguments)
        elif name == "bull_market.evolve":
            result = await _handle_evolve(arguments)
        elif name == "bull_market.full_workflow":
            result = await _handle_full_workflow(arguments)
        else:
            result = {"success": False, "error": f"未知工具: {name}"}
        
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False, indent=2))]
    
    except Exception as e:
        logger.error(f"工具调用失败: {e}", exc_info=True)
        return [TextContent(type="text", text=json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))]


async def _handle_extract_patterns(args: Dict) -> Dict:
    """提取牛市模式"""
    try:
        from core.data_mining.bull_market_high_return_miner import BullMarketHighReturnMiner
        from core.pattern_recognition.bull_market_pattern_extractor import BullMarketPatternExtractor
        
        cases_csv_path = args.get('cases_csv_path')
        output_json_path = args.get('output_json_path', 'data/bull_market_patterns.json')
        
        # 如果没有提供CSV，先挖掘
        if not cases_csv_path or not Path(cases_csv_path).exists():
            logger.info("开始挖掘牛市高回报案例...")
            miner = BullMarketHighReturnMiner(
                min_return_pct=args.get('min_return_pct', 10.0),
                verbose=False
            )
            cases = miner.mine_high_return_cases(
                start_date=args.get('start_date', '2024-09-01'),
                end_date=args.get('end_date', '2025-09-13'),
                min_bull_score=60.0
            )
            cases_csv_path = 'data/bull_market_high_return_cases.csv'
            miner.save_to_csv(cases, cases_csv_path)
        
        # 提取模式
        extractor = BullMarketPatternExtractor(
            n_clusters=args.get('n_clusters', 4),
            verbose=False
        )
        cases_df = extractor.load_cases_from_csv(cases_csv_path)
        patterns = extractor.extract_patterns(cases_df)
        extractor.save_patterns(patterns, output_json_path)
        
        return {
            "success": True,
            "patterns_count": len(patterns),
            "patterns": [p.to_dict() for p in patterns],
            "output_json_path": output_json_path,
        }
    except Exception as e:
        logger.error(f"提取模式失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def _handle_detect_state(args: Dict) -> Dict:
    """检测牛市状态"""
    try:
        from core.market_regime.bull_market_signal_aggregator import BullMarketSignalAggregator
        
        aggregator = BullMarketSignalAggregator(verbose=False)
        signal = aggregator.aggregate(date=args.get('date'))
        
        return {
            "success": True,
            "bull_probability": signal.bull_probability,
            "strength_level": signal.strength_level,
            "strength_score": signal.strength_score,
            "confidence": signal.confidence,
            "position_suggestion": signal.position_suggestion,
            "strategy_suggestion": signal.strategy_suggestion,
            "indicators": signal.indicators.to_dict(),
        }
    except Exception as e:
        logger.error(f"检测牛市状态失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def _handle_generate_strategy(args: Dict) -> Dict:
    """生成策略"""
    try:
        from core.advisor_v4.bullettrade_strategy_generator import BulletTradeStrategyGenerator, StrategyConfig
        
        bull_strength = args.get('bull_strength', 70.0)
        strategy_mode = args.get('strategy_mode', 'AUTO')
        
        # 确定策略模式
        if strategy_mode == 'AUTO':
            if bull_strength > 70.0:
                strategy_mode = 'BULL_AGGRESSIVE'
            elif bull_strength > 30.0:
                strategy_mode = 'BULL_MIXED'
            else:
                strategy_mode = 'BASE_FACTOR'
        
        # 创建配置
        config = StrategyConfig()
        if strategy_mode == 'BULL_AGGRESSIVE':
            config.max_stocks = 15
            config.min_total_score = 28.0
        elif strategy_mode == 'BULL_MIXED':
            config.max_stocks = 12
            config.min_total_score = 30.0
        else:
            config.max_stocks = 10
            config.min_total_score = 30.0
        
        # 生成策略代码
        generator = BulletTradeStrategyGenerator(config=config)
        strategy_code = generator.generate_strategy_code()
        
        # 保存到文件（如果指定）
        output_path = args.get('output_path')
        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            Path(output_path).write_text(strategy_code, encoding='utf-8')
        
        return {
            "success": True,
            "strategy_mode": strategy_mode,
            "strategy_code_length": len(strategy_code),
            "output_path": output_path,
            "params": {
                "max_stocks": config.max_stocks,
                "min_total_score": config.min_total_score,
            }
        }
    except Exception as e:
        logger.error(f"生成策略失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def _handle_backtest(args: Dict) -> Dict:
    """执行回测"""
    try:
        from core.bullettrade.recursive_backtest_engine import RecursiveBacktestEngine, BacktestConfig
        
        backtest_config = BacktestConfig(
            start_date=args.get('start_date', '2024-10-01'),
            end_date=args.get('end_date', '2024-12-31'),
            initial_capital=args.get('initial_capital', 1000000.0),
        )
        
        engine = RecursiveBacktestEngine(
            base_config=backtest_config,
            verbose=False
        )
        
        result = engine.run_backtest(
            strategy_params=args.get('strategy_params', {}),
            strategy_code=args.get('strategy_code'),
            backtest_id=args.get('backtest_id')
        )
        
        return {
            "success": True,
            "result": result.to_dict(),
            "meets_target": result.meets_target(),
        }
    except Exception as e:
        logger.error(f"回测失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def _handle_evolve(args: Dict) -> Dict:
    """递归进化"""
    try:
        from core.evolution.evolution_controller import EvolutionController
        from core.evolution.bull_market_strategy_evolver import EvolutionConfig
        from core.bullettrade.recursive_backtest_engine import BacktestConfig
        
        backtest_config = BacktestConfig(
            start_date=args.get('start_date', '2024-10-01'),
            end_date=args.get('end_date', '2024-12-31'),
            initial_capital=1000000.0,
        )
        
        evolution_config = EvolutionConfig(
            population_size=args.get('population_size', 50),
            generations=args.get('generations', 10),
            target_monthly_return=args.get('target_monthly_return', 0.30),
            max_drawdown_limit=args.get('max_drawdown_limit', -0.20),
            min_sharpe_ratio=args.get('min_sharpe_ratio', 2.0),
        )
        
        controller = EvolutionController(
            backtest_config=backtest_config,
            evolution_config=evolution_config,
            output_dir=args.get('output_dir', 'output/evolution'),
            verbose=True
        )
        
        result = controller.run_evolution()
        
        return {
            "success": True,
            "reached_target": result.reached_target,
            "best_params": result.best_individual.params if result.best_individual else {},
            "best_result": result.best_individual.backtest_result.to_dict() if result.best_individual and result.best_individual.backtest_result else {},
            "total_generations": result.total_generations,
        }
    except Exception as e:
        logger.error(f"进化失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


async def _handle_full_workflow(args: Dict) -> Dict:
    """完整工作流"""
    try:
        from core.workflow.bull_market_strategy_workflow import BullMarketStrategyWorkflow, WorkflowConfig
        
        workflow_config = WorkflowConfig(**args.get('workflow_config', {}))
        workflow = BullMarketStrategyWorkflow(config=workflow_config, verbose=True)
        
        result = workflow.execute(
            skip_mining=args.get('skip_mining', False),
            skip_evolution=args.get('skip_evolution', False)
        )
        
        return {
            "success": True,
            "workflow_id": result.workflow_id,
            "reached_target": result.reached_target,
            "best_strategy_params": result.best_strategy_params,
            "best_backtest_result": result.best_backtest_result,
            "errors": result.errors,
        }
    except Exception as e:
        logger.error(f"工作流执行失败: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


# ==================== 主函数 ====================

async def main():
    """主函数"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
