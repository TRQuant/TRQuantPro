#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股多因子量化系统 - MCP工具
==============================

提供MCP工具接口：
- tenbagger.multifactor.scan - 扫描并打分
- tenbagger.multifactor.score - 单股评分
- tenbagger.multifactor.backtest - 回测
- tenbagger.multifactor.optimize - 参数优化
- tenbagger.multifactor.report - 生成报告

代码位置: mcp_servers/utils/tenbagger_multifactor_tools.py
"""

import sys
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 添加项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# MCP Tool定义
# ============================================================

@dataclass
class Tool:
    """MCP工具定义"""
    name: str
    description: str
    inputSchema: Dict


# 工具列表
TENBAGGER_MULTIFACTOR_TOOLS = [
    Tool(
        name="tenbagger.multifactor.scan",
        description="扫描科技主线股票并进行多因子打分",
        inputSchema={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "扫描日期 (YYYY-MM-DD)，默认今天"
                },
                "top_n": {
                    "type": "integer",
                    "description": "返回Top N股票，默认10",
                    "default": 10
                },
                "min_score": {
                    "type": "number",
                    "description": "最低得分阈值，默认60",
                    "default": 60
                }
            }
        }
    ),
    Tool(
        name="tenbagger.multifactor.signal",
        description="生成每日交易信号（买入/卖出）",
        inputSchema={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "信号日期 (YYYY-MM-DD)"
                },
                "min_momentum": {
                    "type": "number",
                    "description": "最低动量阈值%，默认5",
                    "default": 5
                }
            }
        }
    ),
    Tool(
        name="tenbagger.multifactor.validate",
        description="样本外验证 - 测试策略在未见数据上的表现",
        inputSchema={
            "type": "object",
            "properties": {
                "train_end": {
                    "type": "string",
                    "description": "训练期结束日期"
                },
                "test_start": {
                    "type": "string",
                    "description": "测试期开始日期"
                },
                "test_end": {
                    "type": "string",
                    "description": "测试期结束日期"
                }
            },
            "required": ["train_end", "test_start", "test_end"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.score",
        description="对单只股票进行多因子评分",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代码，如 000001.XSHE"
                },
                "date": {
                    "type": "string",
                    "description": "评分日期 (YYYY-MM-DD)"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.stage",
        description="识别股票所处的成长阶段(S0-S5)",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代码"
                },
                "date": {
                    "type": "string",
                    "description": "识别日期"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.backtest",
        description="运行多因子策略回测",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期 (YYYY-MM-DD)"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期 (YYYY-MM-DD)"
                },
                "initial_capital": {
                    "type": "number",
                    "description": "初始资金",
                    "default": 1000000
                },
                "max_holdings": {
                    "type": "integer",
                    "description": "最大持仓数",
                    "default": 5
                },
                "stop_loss": {
                    "type": "number",
                    "description": "止损比例",
                    "default": -0.10
                },
                "take_profit": {
                    "type": "number",
                    "description": "止盈比例",
                    "default": 0.50
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.optimize",
        description="参数优化 - 网格搜索最优参数组合",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期"
                },
                "param_grid": {
                    "type": "object",
                    "description": "参数网格，如 {max_holdings: [3,5,7], stop_loss: [-0.08,-0.10,-0.12]}"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.report",
        description="生成多因子策略HTML报告",
        inputSchema={
            "type": "object",
            "properties": {
                "scan_date": {
                    "type": "string",
                    "description": "扫描日期"
                },
                "backtest_start": {
                    "type": "string",
                    "description": "回测开始日期"
                },
                "backtest_end": {
                    "type": "string",
                    "description": "回测结束日期"
                }
            }
        }
    ),
]


# ============================================================
# 工具处理函数
# ============================================================

def _get_system(config: Dict = None):
    """获取多因子系统实例"""
    from research.tenbagger_10x_strategy.scripts.tenbagger_multifactor_system import TenbaggerMultifactorSystem
    return TenbaggerMultifactorSystem(config or {})


async def handle_scan(args: Dict) -> Dict:
    """扫描并打分"""
    try:
        date = args.get('date')
        top_n = args.get('top_n', 10)
        min_score = args.get('min_score', 60)
        
        system = _get_system()
        results = system.scan_and_score(date)
        
        # 过滤并返回Top N
        filtered = [r for r in results if r['total_score'] >= min_score][:top_n]
        
        return {
            "success": True,
            "total_scanned": len(results),
            "filtered_count": len(filtered),
            "candidates": [
                {
                    "symbol": r['symbol'],
                    "name": r['name'],
                    "score": r['total_score'],
                    "stage": r['stage'],
                    "grade": r['scorecard_grade'],
                    "recommendation": r['recommendation']
                }
                for r in filtered
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_score(args: Dict) -> Dict:
    """单股评分"""
    try:
        symbol = args['symbol']
        date = args.get('date')
        
        system = _get_system()
        if not system.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        data = system.fetch_stock_data(symbol, date)
        result = system.scorer.score(symbol, data.get('name', ''), data)
        
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_stage(args: Dict) -> Dict:
    """阶段识别"""
    try:
        symbol = args['symbol']
        date = args.get('date')
        
        system = _get_system()
        if not system.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        data = system.fetch_stock_data(symbol, date)
        stage, confidence, signals = system.scorer.stage_identifier.identify(data)
        
        return {
            "success": True,
            "symbol": symbol,
            "stage": stage.value,
            "confidence": confidence,
            "signals": signals,
            "description": {
                "S0": "观察期 - 有产业链位置，无明显兑现信号",
                "S1": "验证期 - 送样/认证中，尚未确认客户",
                "S2": "导入期 - 已进入客户体系，最佳介入点",
                "S3": "放量期 - 批量订单，扩产明确",
                "S4": "加速期 - 业绩拐点，估值修复",
                "S5": "成熟期 - 主流共识，十倍股特征消失"
            }.get(stage.value, "")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_backtest(args: Dict) -> Dict:
    """回测"""
    try:
        # 使用验证有效的最优参数
        config = {
            'max_holdings': args.get('max_holdings', 2),  # 集中持仓
            'momentum_period': args.get('momentum_period', 20),
            'rebalance_days': args.get('rebalance_days', 3),  # 3日调仓
            'stop_loss': args.get('stop_loss', -0.08),  # -8%止损
            'take_profit': args.get('take_profit', 0.50),  # 50%止盈
        }
        
        # 优先使用快速优化版
        try:
            from research.tenbagger_10x_strategy.scripts.tenbagger_fast_optimize import vectorized_backtest, authenticate_jqdata
            import jqdatasdk as jq
            from datetime import datetime, timedelta
            
            if authenticate_jqdata():
                stocks = jq.get_index_stocks('399006.XSHE')[:50]
                stocks += jq.get_index_stocks('000905.XSHG')[:30]
                stocks = list(set(stocks))
                
                price_data = jq.get_price(
                    stocks,
                    start_date=(datetime.strptime(args['start_date'], '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
                    end_date=args['end_date'],
                    frequency='daily',
                    fields=['close'],
                    panel=False,
                    skip_paused=True
                )
                
                results = vectorized_backtest(price_data, config)
                jq.logout()
                
                return {
                    "success": True,
                    "metrics": results['metrics'],
                    "trade_count": len(results.get('trades', [])),
                    "config": config
                }
        except Exception as e:
            logger.warning(f"快速回测失败，回退到原版: {e}")
        
        # 回退到原版
        system = _get_system(config)
        results = system.run_backtest(
            start_date=args['start_date'],
            end_date=args['end_date'],
            initial_capital=args.get('initial_capital', 1000000)
        )
        
        if results['success']:
            return {
                "success": True,
                "metrics": results['metrics'],
                "trade_count": results.get('trade_count', 0)
            }
        else:
            return results
            
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_optimize(args: Dict) -> Dict:
    """参数优化"""
    try:
        start_date = args['start_date']
        end_date = args['end_date']
        param_grid = args.get('param_grid', {
            'max_holdings': [3, 5],
            'stop_loss': [-0.08, -0.10, -0.12],
            'take_profit': [0.30, 0.50, 0.80]
        })
        
        best_result = None
        best_sharpe = -float('inf')
        all_results = []
        
        # 网格搜索
        from itertools import product
        
        keys = list(param_grid.keys())
        values = list(param_grid.values())
        
        for combo in product(*values):
            config = dict(zip(keys, combo))
            
            system = _get_system(config)
            result = system.run_backtest(start_date, end_date)
            
            if result['success']:
                sharpe = result['metrics'].get('sharpe_ratio', 0)
                all_results.append({
                    'params': config,
                    'sharpe': sharpe,
                    'total_return': result['metrics'].get('total_return', 0),
                    'max_drawdown': result['metrics'].get('max_drawdown', 0)
                })
                
                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best_result = {
                        'params': config,
                        'metrics': result['metrics']
                    }
        
        return {
            "success": True,
            "best_params": best_result['params'] if best_result else {},
            "best_metrics": best_result['metrics'] if best_result else {},
            "all_results": sorted(all_results, key=lambda x: x['sharpe'], reverse=True)[:10]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_report(args: Dict) -> Dict:
    """生成报告"""
    try:
        scan_date = args.get('scan_date')
        backtest_start = args.get('backtest_start', '2024-01-01')
        backtest_end = args.get('backtest_end', '2025-12-20')
        
        system = _get_system()
        
        # 扫描
        scan_results = system.scan_and_score(scan_date)
        
        # 回测
        backtest_results = system.run_backtest(backtest_start, backtest_end)
        
        # 生成报告
        html = system.generate_report(scan_results, backtest_results)
        
        # 保存
        from datetime import datetime
        reports_dir = PROJECT_ROOT / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"tenbagger_multifactor_{timestamp}.html"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "metrics": backtest_results.get('metrics', {}),
            "top_candidates": [
                {"symbol": r['symbol'], "name": r['name'], "score": r['total_score']}
                for r in system.get_top_candidates(scan_results, 5)
            ]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
async def handle_signal(args: Dict) -> Dict:
    """生成交易信号"""
    try:
        from research.tenbagger_10x_strategy.scripts.tenbagger_signal_generator import TenbaggerSignalGenerator, SignalConfig
        from dataclasses import asdict
        
        config = SignalConfig(
            min_momentum=args.get('min_momentum', 5)
        )
        
        generator = TenbaggerSignalGenerator(config)
        signals = generator.generate_buy_signals(args.get('date'))
        
        return {
            "success": True,
            "date": args.get('date', 'today'),
            "signal_count": len(signals),
            "signals": [asdict(s) for s in signals]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_validate(args: Dict) -> Dict:
    """样本外验证"""
    try:
        from research.tenbagger_10x_strategy.scripts.tenbagger_signal_generator import TenbaggerSignalGenerator
        
        generator = TenbaggerSignalGenerator()
        result = generator.validate_out_of_sample(
            train_end=args['train_end'],
            test_start=args['test_start'],
            test_end=args['test_end']
        )
        
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
# 处理函数映射
# ============================================================

TENBAGGER_MULTIFACTOR_HANDLERS = {
    "tenbagger.multifactor.scan": handle_scan,
    "tenbagger.multifactor.score": handle_score,
    "tenbagger.multifactor.stage": handle_stage,
    "tenbagger.multifactor.backtest": handle_backtest,
    "tenbagger.multifactor.optimize": handle_optimize,
    "tenbagger.multifactor.report": handle_report,
    "tenbagger.multifactor.signal": handle_signal,
    "tenbagger.multifactor.validate": handle_validate,
}


# ============================================================
# 导出
# ============================================================

def get_tools():
    """获取工具列表"""
    return TENBAGGER_MULTIFACTOR_TOOLS


def get_handlers():
    """获取处理函数"""
    return TENBAGGER_MULTIFACTOR_HANDLERS


async def call_tool(name: str, args: Dict) -> Dict:
    """调用工具"""
    handler = TENBAGGER_MULTIFACTOR_HANDLERS.get(name)
    if handler:
        return await handler(args)
    return {"success": False, "error": f"Unknown tool: {name}"}


"""
十倍股多因子量化系统 - MCP工具
==============================

提供MCP工具接口：
- tenbagger.multifactor.scan - 扫描并打分
- tenbagger.multifactor.score - 单股评分
- tenbagger.multifactor.backtest - 回测
- tenbagger.multifactor.optimize - 参数优化
- tenbagger.multifactor.report - 生成报告

代码位置: mcp_servers/utils/tenbagger_multifactor_tools.py
"""

import sys
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 添加项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# MCP Tool定义
# ============================================================

@dataclass
class Tool:
    """MCP工具定义"""
    name: str
    description: str
    inputSchema: Dict


# 工具列表
TENBAGGER_MULTIFACTOR_TOOLS = [
    Tool(
        name="tenbagger.multifactor.scan",
        description="扫描科技主线股票并进行多因子打分",
        inputSchema={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "扫描日期 (YYYY-MM-DD)，默认今天"
                },
                "top_n": {
                    "type": "integer",
                    "description": "返回Top N股票，默认10",
                    "default": 10
                },
                "min_score": {
                    "type": "number",
                    "description": "最低得分阈值，默认60",
                    "default": 60
                }
            }
        }
    ),
    Tool(
        name="tenbagger.multifactor.signal",
        description="生成每日交易信号（买入/卖出）",
        inputSchema={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "信号日期 (YYYY-MM-DD)"
                },
                "min_momentum": {
                    "type": "number",
                    "description": "最低动量阈值%，默认5",
                    "default": 5
                }
            }
        }
    ),
    Tool(
        name="tenbagger.multifactor.validate",
        description="样本外验证 - 测试策略在未见数据上的表现",
        inputSchema={
            "type": "object",
            "properties": {
                "train_end": {
                    "type": "string",
                    "description": "训练期结束日期"
                },
                "test_start": {
                    "type": "string",
                    "description": "测试期开始日期"
                },
                "test_end": {
                    "type": "string",
                    "description": "测试期结束日期"
                }
            },
            "required": ["train_end", "test_start", "test_end"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.score",
        description="对单只股票进行多因子评分",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代码，如 000001.XSHE"
                },
                "date": {
                    "type": "string",
                    "description": "评分日期 (YYYY-MM-DD)"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.stage",
        description="识别股票所处的成长阶段(S0-S5)",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代码"
                },
                "date": {
                    "type": "string",
                    "description": "识别日期"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.backtest",
        description="运行多因子策略回测",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期 (YYYY-MM-DD)"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期 (YYYY-MM-DD)"
                },
                "initial_capital": {
                    "type": "number",
                    "description": "初始资金",
                    "default": 1000000
                },
                "max_holdings": {
                    "type": "integer",
                    "description": "最大持仓数",
                    "default": 5
                },
                "stop_loss": {
                    "type": "number",
                    "description": "止损比例",
                    "default": -0.10
                },
                "take_profit": {
                    "type": "number",
                    "description": "止盈比例",
                    "default": 0.50
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.optimize",
        description="参数优化 - 网格搜索最优参数组合",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期"
                },
                "param_grid": {
                    "type": "object",
                    "description": "参数网格，如 {max_holdings: [3,5,7], stop_loss: [-0.08,-0.10,-0.12]}"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.report",
        description="生成多因子策略HTML报告",
        inputSchema={
            "type": "object",
            "properties": {
                "scan_date": {
                    "type": "string",
                    "description": "扫描日期"
                },
                "backtest_start": {
                    "type": "string",
                    "description": "回测开始日期"
                },
                "backtest_end": {
                    "type": "string",
                    "description": "回测结束日期"
                }
            }
        }
    ),
]


# ============================================================
# 工具处理函数
# ============================================================

def _get_system(config: Dict = None):
    """获取多因子系统实例"""
    from research.tenbagger_10x_strategy.scripts.tenbagger_multifactor_system import TenbaggerMultifactorSystem
    return TenbaggerMultifactorSystem(config or {})


async def handle_scan(args: Dict) -> Dict:
    """扫描并打分"""
    try:
        date = args.get('date')
        top_n = args.get('top_n', 10)
        min_score = args.get('min_score', 60)
        
        system = _get_system()
        results = system.scan_and_score(date)
        
        # 过滤并返回Top N
        filtered = [r for r in results if r['total_score'] >= min_score][:top_n]
        
        return {
            "success": True,
            "total_scanned": len(results),
            "filtered_count": len(filtered),
            "candidates": [
                {
                    "symbol": r['symbol'],
                    "name": r['name'],
                    "score": r['total_score'],
                    "stage": r['stage'],
                    "grade": r['scorecard_grade'],
                    "recommendation": r['recommendation']
                }
                for r in filtered
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_score(args: Dict) -> Dict:
    """单股评分"""
    try:
        symbol = args['symbol']
        date = args.get('date')
        
        system = _get_system()
        if not system.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        data = system.fetch_stock_data(symbol, date)
        result = system.scorer.score(symbol, data.get('name', ''), data)
        
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_stage(args: Dict) -> Dict:
    """阶段识别"""
    try:
        symbol = args['symbol']
        date = args.get('date')
        
        system = _get_system()
        if not system.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        data = system.fetch_stock_data(symbol, date)
        stage, confidence, signals = system.scorer.stage_identifier.identify(data)
        
        return {
            "success": True,
            "symbol": symbol,
            "stage": stage.value,
            "confidence": confidence,
            "signals": signals,
            "description": {
                "S0": "观察期 - 有产业链位置，无明显兑现信号",
                "S1": "验证期 - 送样/认证中，尚未确认客户",
                "S2": "导入期 - 已进入客户体系，最佳介入点",
                "S3": "放量期 - 批量订单，扩产明确",
                "S4": "加速期 - 业绩拐点，估值修复",
                "S5": "成熟期 - 主流共识，十倍股特征消失"
            }.get(stage.value, "")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_backtest(args: Dict) -> Dict:
    """回测"""
    try:
        # 使用验证有效的最优参数
        config = {
            'max_holdings': args.get('max_holdings', 2),  # 集中持仓
            'momentum_period': args.get('momentum_period', 20),
            'rebalance_days': args.get('rebalance_days', 3),  # 3日调仓
            'stop_loss': args.get('stop_loss', -0.08),  # -8%止损
            'take_profit': args.get('take_profit', 0.50),  # 50%止盈
        }
        
        # 优先使用快速优化版
        try:
            from research.tenbagger_10x_strategy.scripts.tenbagger_fast_optimize import vectorized_backtest, authenticate_jqdata
            import jqdatasdk as jq
            from datetime import datetime, timedelta
            
            if authenticate_jqdata():
                stocks = jq.get_index_stocks('399006.XSHE')[:50]
                stocks += jq.get_index_stocks('000905.XSHG')[:30]
                stocks = list(set(stocks))
                
                price_data = jq.get_price(
                    stocks,
                    start_date=(datetime.strptime(args['start_date'], '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
                    end_date=args['end_date'],
                    frequency='daily',
                    fields=['close'],
                    panel=False,
                    skip_paused=True
                )
                
                results = vectorized_backtest(price_data, config)
                jq.logout()
                
                return {
                    "success": True,
                    "metrics": results['metrics'],
                    "trade_count": len(results.get('trades', [])),
                    "config": config
                }
        except Exception as e:
            logger.warning(f"快速回测失败，回退到原版: {e}")
        
        # 回退到原版
        system = _get_system(config)
        results = system.run_backtest(
            start_date=args['start_date'],
            end_date=args['end_date'],
            initial_capital=args.get('initial_capital', 1000000)
        )
        
        if results['success']:
            return {
                "success": True,
                "metrics": results['metrics'],
                "trade_count": results.get('trade_count', 0)
            }
        else:
            return results
            
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_optimize(args: Dict) -> Dict:
    """参数优化"""
    try:
        start_date = args['start_date']
        end_date = args['end_date']
        param_grid = args.get('param_grid', {
            'max_holdings': [3, 5],
            'stop_loss': [-0.08, -0.10, -0.12],
            'take_profit': [0.30, 0.50, 0.80]
        })
        
        best_result = None
        best_sharpe = -float('inf')
        all_results = []
        
        # 网格搜索
        from itertools import product
        
        keys = list(param_grid.keys())
        values = list(param_grid.values())
        
        for combo in product(*values):
            config = dict(zip(keys, combo))
            
            system = _get_system(config)
            result = system.run_backtest(start_date, end_date)
            
            if result['success']:
                sharpe = result['metrics'].get('sharpe_ratio', 0)
                all_results.append({
                    'params': config,
                    'sharpe': sharpe,
                    'total_return': result['metrics'].get('total_return', 0),
                    'max_drawdown': result['metrics'].get('max_drawdown', 0)
                })
                
                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best_result = {
                        'params': config,
                        'metrics': result['metrics']
                    }
        
        return {
            "success": True,
            "best_params": best_result['params'] if best_result else {},
            "best_metrics": best_result['metrics'] if best_result else {},
            "all_results": sorted(all_results, key=lambda x: x['sharpe'], reverse=True)[:10]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_report(args: Dict) -> Dict:
    """生成报告"""
    try:
        scan_date = args.get('scan_date')
        backtest_start = args.get('backtest_start', '2024-01-01')
        backtest_end = args.get('backtest_end', '2025-12-20')
        
        system = _get_system()
        
        # 扫描
        scan_results = system.scan_and_score(scan_date)
        
        # 回测
        backtest_results = system.run_backtest(backtest_start, backtest_end)
        
        # 生成报告
        html = system.generate_report(scan_results, backtest_results)
        
        # 保存
        from datetime import datetime
        reports_dir = PROJECT_ROOT / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"tenbagger_multifactor_{timestamp}.html"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "metrics": backtest_results.get('metrics', {}),
            "top_candidates": [
                {"symbol": r['symbol'], "name": r['name'], "score": r['total_score']}
                for r in system.get_top_candidates(scan_results, 5)
            ]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
async def handle_signal(args: Dict) -> Dict:
    """生成交易信号"""
    try:
        from research.tenbagger_10x_strategy.scripts.tenbagger_signal_generator import TenbaggerSignalGenerator, SignalConfig
        from dataclasses import asdict
        
        config = SignalConfig(
            min_momentum=args.get('min_momentum', 5)
        )
        
        generator = TenbaggerSignalGenerator(config)
        signals = generator.generate_buy_signals(args.get('date'))
        
        return {
            "success": True,
            "date": args.get('date', 'today'),
            "signal_count": len(signals),
            "signals": [asdict(s) for s in signals]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_validate(args: Dict) -> Dict:
    """样本外验证"""
    try:
        from research.tenbagger_10x_strategy.scripts.tenbagger_signal_generator import TenbaggerSignalGenerator
        
        generator = TenbaggerSignalGenerator()
        result = generator.validate_out_of_sample(
            train_end=args['train_end'],
            test_start=args['test_start'],
            test_end=args['test_end']
        )
        
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
# 处理函数映射
# ============================================================

TENBAGGER_MULTIFACTOR_HANDLERS = {
    "tenbagger.multifactor.scan": handle_scan,
    "tenbagger.multifactor.score": handle_score,
    "tenbagger.multifactor.stage": handle_stage,
    "tenbagger.multifactor.backtest": handle_backtest,
    "tenbagger.multifactor.optimize": handle_optimize,
    "tenbagger.multifactor.report": handle_report,
    "tenbagger.multifactor.signal": handle_signal,
    "tenbagger.multifactor.validate": handle_validate,
}


# ============================================================
# 导出
# ============================================================

def get_tools():
    """获取工具列表"""
    return TENBAGGER_MULTIFACTOR_TOOLS


def get_handlers():
    """获取处理函数"""
    return TENBAGGER_MULTIFACTOR_HANDLERS


async def call_tool(name: str, args: Dict) -> Dict:
    """调用工具"""
    handler = TENBAGGER_MULTIFACTOR_HANDLERS.get(name)
    if handler:
        return await handler(args)
    return {"success": False, "error": f"Unknown tool: {name}"}


"""
十倍股多因子量化系统 - MCP工具
==============================

提供MCP工具接口：
- tenbagger.multifactor.scan - 扫描并打分
- tenbagger.multifactor.score - 单股评分
- tenbagger.multifactor.backtest - 回测
- tenbagger.multifactor.optimize - 参数优化
- tenbagger.multifactor.report - 生成报告

代码位置: mcp_servers/utils/tenbagger_multifactor_tools.py
"""

import sys
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 添加项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# MCP Tool定义
# ============================================================

@dataclass
class Tool:
    """MCP工具定义"""
    name: str
    description: str
    inputSchema: Dict


# 工具列表
TENBAGGER_MULTIFACTOR_TOOLS = [
    Tool(
        name="tenbagger.multifactor.scan",
        description="扫描科技主线股票并进行多因子打分",
        inputSchema={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "扫描日期 (YYYY-MM-DD)，默认今天"
                },
                "top_n": {
                    "type": "integer",
                    "description": "返回Top N股票，默认10",
                    "default": 10
                },
                "min_score": {
                    "type": "number",
                    "description": "最低得分阈值，默认60",
                    "default": 60
                }
            }
        }
    ),
    Tool(
        name="tenbagger.multifactor.signal",
        description="生成每日交易信号（买入/卖出）",
        inputSchema={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "信号日期 (YYYY-MM-DD)"
                },
                "min_momentum": {
                    "type": "number",
                    "description": "最低动量阈值%，默认5",
                    "default": 5
                }
            }
        }
    ),
    Tool(
        name="tenbagger.multifactor.validate",
        description="样本外验证 - 测试策略在未见数据上的表现",
        inputSchema={
            "type": "object",
            "properties": {
                "train_end": {
                    "type": "string",
                    "description": "训练期结束日期"
                },
                "test_start": {
                    "type": "string",
                    "description": "测试期开始日期"
                },
                "test_end": {
                    "type": "string",
                    "description": "测试期结束日期"
                }
            },
            "required": ["train_end", "test_start", "test_end"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.score",
        description="对单只股票进行多因子评分",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代码，如 000001.XSHE"
                },
                "date": {
                    "type": "string",
                    "description": "评分日期 (YYYY-MM-DD)"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.stage",
        description="识别股票所处的成长阶段(S0-S5)",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代码"
                },
                "date": {
                    "type": "string",
                    "description": "识别日期"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.backtest",
        description="运行多因子策略回测",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期 (YYYY-MM-DD)"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期 (YYYY-MM-DD)"
                },
                "initial_capital": {
                    "type": "number",
                    "description": "初始资金",
                    "default": 1000000
                },
                "max_holdings": {
                    "type": "integer",
                    "description": "最大持仓数",
                    "default": 5
                },
                "stop_loss": {
                    "type": "number",
                    "description": "止损比例",
                    "default": -0.10
                },
                "take_profit": {
                    "type": "number",
                    "description": "止盈比例",
                    "default": 0.50
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.optimize",
        description="参数优化 - 网格搜索最优参数组合",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期"
                },
                "param_grid": {
                    "type": "object",
                    "description": "参数网格，如 {max_holdings: [3,5,7], stop_loss: [-0.08,-0.10,-0.12]}"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.report",
        description="生成多因子策略HTML报告",
        inputSchema={
            "type": "object",
            "properties": {
                "scan_date": {
                    "type": "string",
                    "description": "扫描日期"
                },
                "backtest_start": {
                    "type": "string",
                    "description": "回测开始日期"
                },
                "backtest_end": {
                    "type": "string",
                    "description": "回测结束日期"
                }
            }
        }
    ),
]


# ============================================================
# 工具处理函数
# ============================================================

def _get_system(config: Dict = None):
    """获取多因子系统实例"""
    from research.tenbagger_10x_strategy.scripts.tenbagger_multifactor_system import TenbaggerMultifactorSystem
    return TenbaggerMultifactorSystem(config or {})


async def handle_scan(args: Dict) -> Dict:
    """扫描并打分"""
    try:
        date = args.get('date')
        top_n = args.get('top_n', 10)
        min_score = args.get('min_score', 60)
        
        system = _get_system()
        results = system.scan_and_score(date)
        
        # 过滤并返回Top N
        filtered = [r for r in results if r['total_score'] >= min_score][:top_n]
        
        return {
            "success": True,
            "total_scanned": len(results),
            "filtered_count": len(filtered),
            "candidates": [
                {
                    "symbol": r['symbol'],
                    "name": r['name'],
                    "score": r['total_score'],
                    "stage": r['stage'],
                    "grade": r['scorecard_grade'],
                    "recommendation": r['recommendation']
                }
                for r in filtered
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_score(args: Dict) -> Dict:
    """单股评分"""
    try:
        symbol = args['symbol']
        date = args.get('date')
        
        system = _get_system()
        if not system.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        data = system.fetch_stock_data(symbol, date)
        result = system.scorer.score(symbol, data.get('name', ''), data)
        
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_stage(args: Dict) -> Dict:
    """阶段识别"""
    try:
        symbol = args['symbol']
        date = args.get('date')
        
        system = _get_system()
        if not system.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        data = system.fetch_stock_data(symbol, date)
        stage, confidence, signals = system.scorer.stage_identifier.identify(data)
        
        return {
            "success": True,
            "symbol": symbol,
            "stage": stage.value,
            "confidence": confidence,
            "signals": signals,
            "description": {
                "S0": "观察期 - 有产业链位置，无明显兑现信号",
                "S1": "验证期 - 送样/认证中，尚未确认客户",
                "S2": "导入期 - 已进入客户体系，最佳介入点",
                "S3": "放量期 - 批量订单，扩产明确",
                "S4": "加速期 - 业绩拐点，估值修复",
                "S5": "成熟期 - 主流共识，十倍股特征消失"
            }.get(stage.value, "")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_backtest(args: Dict) -> Dict:
    """回测"""
    try:
        # 使用验证有效的最优参数
        config = {
            'max_holdings': args.get('max_holdings', 2),  # 集中持仓
            'momentum_period': args.get('momentum_period', 20),
            'rebalance_days': args.get('rebalance_days', 3),  # 3日调仓
            'stop_loss': args.get('stop_loss', -0.08),  # -8%止损
            'take_profit': args.get('take_profit', 0.50),  # 50%止盈
        }
        
        # 优先使用快速优化版
        try:
            from research.tenbagger_10x_strategy.scripts.tenbagger_fast_optimize import vectorized_backtest, authenticate_jqdata
            import jqdatasdk as jq
            from datetime import datetime, timedelta
            
            if authenticate_jqdata():
                stocks = jq.get_index_stocks('399006.XSHE')[:50]
                stocks += jq.get_index_stocks('000905.XSHG')[:30]
                stocks = list(set(stocks))
                
                price_data = jq.get_price(
                    stocks,
                    start_date=(datetime.strptime(args['start_date'], '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
                    end_date=args['end_date'],
                    frequency='daily',
                    fields=['close'],
                    panel=False,
                    skip_paused=True
                )
                
                results = vectorized_backtest(price_data, config)
                jq.logout()
                
                return {
                    "success": True,
                    "metrics": results['metrics'],
                    "trade_count": len(results.get('trades', [])),
                    "config": config
                }
        except Exception as e:
            logger.warning(f"快速回测失败，回退到原版: {e}")
        
        # 回退到原版
        system = _get_system(config)
        results = system.run_backtest(
            start_date=args['start_date'],
            end_date=args['end_date'],
            initial_capital=args.get('initial_capital', 1000000)
        )
        
        if results['success']:
            return {
                "success": True,
                "metrics": results['metrics'],
                "trade_count": results.get('trade_count', 0)
            }
        else:
            return results
            
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_optimize(args: Dict) -> Dict:
    """参数优化"""
    try:
        start_date = args['start_date']
        end_date = args['end_date']
        param_grid = args.get('param_grid', {
            'max_holdings': [3, 5],
            'stop_loss': [-0.08, -0.10, -0.12],
            'take_profit': [0.30, 0.50, 0.80]
        })
        
        best_result = None
        best_sharpe = -float('inf')
        all_results = []
        
        # 网格搜索
        from itertools import product
        
        keys = list(param_grid.keys())
        values = list(param_grid.values())
        
        for combo in product(*values):
            config = dict(zip(keys, combo))
            
            system = _get_system(config)
            result = system.run_backtest(start_date, end_date)
            
            if result['success']:
                sharpe = result['metrics'].get('sharpe_ratio', 0)
                all_results.append({
                    'params': config,
                    'sharpe': sharpe,
                    'total_return': result['metrics'].get('total_return', 0),
                    'max_drawdown': result['metrics'].get('max_drawdown', 0)
                })
                
                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best_result = {
                        'params': config,
                        'metrics': result['metrics']
                    }
        
        return {
            "success": True,
            "best_params": best_result['params'] if best_result else {},
            "best_metrics": best_result['metrics'] if best_result else {},
            "all_results": sorted(all_results, key=lambda x: x['sharpe'], reverse=True)[:10]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_report(args: Dict) -> Dict:
    """生成报告"""
    try:
        scan_date = args.get('scan_date')
        backtest_start = args.get('backtest_start', '2024-01-01')
        backtest_end = args.get('backtest_end', '2025-12-20')
        
        system = _get_system()
        
        # 扫描
        scan_results = system.scan_and_score(scan_date)
        
        # 回测
        backtest_results = system.run_backtest(backtest_start, backtest_end)
        
        # 生成报告
        html = system.generate_report(scan_results, backtest_results)
        
        # 保存
        from datetime import datetime
        reports_dir = PROJECT_ROOT / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"tenbagger_multifactor_{timestamp}.html"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "metrics": backtest_results.get('metrics', {}),
            "top_candidates": [
                {"symbol": r['symbol'], "name": r['name'], "score": r['total_score']}
                for r in system.get_top_candidates(scan_results, 5)
            ]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
async def handle_signal(args: Dict) -> Dict:
    """生成交易信号"""
    try:
        from research.tenbagger_10x_strategy.scripts.tenbagger_signal_generator import TenbaggerSignalGenerator, SignalConfig
        from dataclasses import asdict
        
        config = SignalConfig(
            min_momentum=args.get('min_momentum', 5)
        )
        
        generator = TenbaggerSignalGenerator(config)
        signals = generator.generate_buy_signals(args.get('date'))
        
        return {
            "success": True,
            "date": args.get('date', 'today'),
            "signal_count": len(signals),
            "signals": [asdict(s) for s in signals]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_validate(args: Dict) -> Dict:
    """样本外验证"""
    try:
        from research.tenbagger_10x_strategy.scripts.tenbagger_signal_generator import TenbaggerSignalGenerator
        
        generator = TenbaggerSignalGenerator()
        result = generator.validate_out_of_sample(
            train_end=args['train_end'],
            test_start=args['test_start'],
            test_end=args['test_end']
        )
        
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
# 处理函数映射
# ============================================================

TENBAGGER_MULTIFACTOR_HANDLERS = {
    "tenbagger.multifactor.scan": handle_scan,
    "tenbagger.multifactor.score": handle_score,
    "tenbagger.multifactor.stage": handle_stage,
    "tenbagger.multifactor.backtest": handle_backtest,
    "tenbagger.multifactor.optimize": handle_optimize,
    "tenbagger.multifactor.report": handle_report,
    "tenbagger.multifactor.signal": handle_signal,
    "tenbagger.multifactor.validate": handle_validate,
}


# ============================================================
# 导出
# ============================================================

def get_tools():
    """获取工具列表"""
    return TENBAGGER_MULTIFACTOR_TOOLS


def get_handlers():
    """获取处理函数"""
    return TENBAGGER_MULTIFACTOR_HANDLERS


async def call_tool(name: str, args: Dict) -> Dict:
    """调用工具"""
    handler = TENBAGGER_MULTIFACTOR_HANDLERS.get(name)
    if handler:
        return await handler(args)
    return {"success": False, "error": f"Unknown tool: {name}"}


"""
十倍股多因子量化系统 - MCP工具
==============================

提供MCP工具接口：
- tenbagger.multifactor.scan - 扫描并打分
- tenbagger.multifactor.score - 单股评分
- tenbagger.multifactor.backtest - 回测
- tenbagger.multifactor.optimize - 参数优化
- tenbagger.multifactor.report - 生成报告

代码位置: mcp_servers/utils/tenbagger_multifactor_tools.py
"""

import sys
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# 添加项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# MCP Tool定义
# ============================================================

@dataclass
class Tool:
    """MCP工具定义"""
    name: str
    description: str
    inputSchema: Dict


# 工具列表
TENBAGGER_MULTIFACTOR_TOOLS = [
    Tool(
        name="tenbagger.multifactor.scan",
        description="扫描科技主线股票并进行多因子打分",
        inputSchema={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "扫描日期 (YYYY-MM-DD)，默认今天"
                },
                "top_n": {
                    "type": "integer",
                    "description": "返回Top N股票，默认10",
                    "default": 10
                },
                "min_score": {
                    "type": "number",
                    "description": "最低得分阈值，默认60",
                    "default": 60
                }
            }
        }
    ),
    Tool(
        name="tenbagger.multifactor.signal",
        description="生成每日交易信号（买入/卖出）",
        inputSchema={
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "信号日期 (YYYY-MM-DD)"
                },
                "min_momentum": {
                    "type": "number",
                    "description": "最低动量阈值%，默认5",
                    "default": 5
                }
            }
        }
    ),
    Tool(
        name="tenbagger.multifactor.validate",
        description="样本外验证 - 测试策略在未见数据上的表现",
        inputSchema={
            "type": "object",
            "properties": {
                "train_end": {
                    "type": "string",
                    "description": "训练期结束日期"
                },
                "test_start": {
                    "type": "string",
                    "description": "测试期开始日期"
                },
                "test_end": {
                    "type": "string",
                    "description": "测试期结束日期"
                }
            },
            "required": ["train_end", "test_start", "test_end"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.score",
        description="对单只股票进行多因子评分",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代码，如 000001.XSHE"
                },
                "date": {
                    "type": "string",
                    "description": "评分日期 (YYYY-MM-DD)"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.stage",
        description="识别股票所处的成长阶段(S0-S5)",
        inputSchema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "股票代码"
                },
                "date": {
                    "type": "string",
                    "description": "识别日期"
                }
            },
            "required": ["symbol"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.backtest",
        description="运行多因子策略回测",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期 (YYYY-MM-DD)"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期 (YYYY-MM-DD)"
                },
                "initial_capital": {
                    "type": "number",
                    "description": "初始资金",
                    "default": 1000000
                },
                "max_holdings": {
                    "type": "integer",
                    "description": "最大持仓数",
                    "default": 5
                },
                "stop_loss": {
                    "type": "number",
                    "description": "止损比例",
                    "default": -0.10
                },
                "take_profit": {
                    "type": "number",
                    "description": "止盈比例",
                    "default": 0.50
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.optimize",
        description="参数优化 - 网格搜索最优参数组合",
        inputSchema={
            "type": "object",
            "properties": {
                "start_date": {
                    "type": "string",
                    "description": "开始日期"
                },
                "end_date": {
                    "type": "string",
                    "description": "结束日期"
                },
                "param_grid": {
                    "type": "object",
                    "description": "参数网格，如 {max_holdings: [3,5,7], stop_loss: [-0.08,-0.10,-0.12]}"
                }
            },
            "required": ["start_date", "end_date"]
        }
    ),
    Tool(
        name="tenbagger.multifactor.report",
        description="生成多因子策略HTML报告",
        inputSchema={
            "type": "object",
            "properties": {
                "scan_date": {
                    "type": "string",
                    "description": "扫描日期"
                },
                "backtest_start": {
                    "type": "string",
                    "description": "回测开始日期"
                },
                "backtest_end": {
                    "type": "string",
                    "description": "回测结束日期"
                }
            }
        }
    ),
]


# ============================================================
# 工具处理函数
# ============================================================

def _get_system(config: Dict = None):
    """获取多因子系统实例"""
    from research.tenbagger_10x_strategy.scripts.tenbagger_multifactor_system import TenbaggerMultifactorSystem
    return TenbaggerMultifactorSystem(config or {})


async def handle_scan(args: Dict) -> Dict:
    """扫描并打分"""
    try:
        date = args.get('date')
        top_n = args.get('top_n', 10)
        min_score = args.get('min_score', 60)
        
        system = _get_system()
        results = system.scan_and_score(date)
        
        # 过滤并返回Top N
        filtered = [r for r in results if r['total_score'] >= min_score][:top_n]
        
        return {
            "success": True,
            "total_scanned": len(results),
            "filtered_count": len(filtered),
            "candidates": [
                {
                    "symbol": r['symbol'],
                    "name": r['name'],
                    "score": r['total_score'],
                    "stage": r['stage'],
                    "grade": r['scorecard_grade'],
                    "recommendation": r['recommendation']
                }
                for r in filtered
            ]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_score(args: Dict) -> Dict:
    """单股评分"""
    try:
        symbol = args['symbol']
        date = args.get('date')
        
        system = _get_system()
        if not system.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        data = system.fetch_stock_data(symbol, date)
        result = system.scorer.score(symbol, data.get('name', ''), data)
        
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_stage(args: Dict) -> Dict:
    """阶段识别"""
    try:
        symbol = args['symbol']
        date = args.get('date')
        
        system = _get_system()
        if not system.authenticate_jqdata():
            return {"success": False, "error": "JQData认证失败"}
        
        data = system.fetch_stock_data(symbol, date)
        stage, confidence, signals = system.scorer.stage_identifier.identify(data)
        
        return {
            "success": True,
            "symbol": symbol,
            "stage": stage.value,
            "confidence": confidence,
            "signals": signals,
            "description": {
                "S0": "观察期 - 有产业链位置，无明显兑现信号",
                "S1": "验证期 - 送样/认证中，尚未确认客户",
                "S2": "导入期 - 已进入客户体系，最佳介入点",
                "S3": "放量期 - 批量订单，扩产明确",
                "S4": "加速期 - 业绩拐点，估值修复",
                "S5": "成熟期 - 主流共识，十倍股特征消失"
            }.get(stage.value, "")
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_backtest(args: Dict) -> Dict:
    """回测"""
    try:
        # 使用验证有效的最优参数
        config = {
            'max_holdings': args.get('max_holdings', 2),  # 集中持仓
            'momentum_period': args.get('momentum_period', 20),
            'rebalance_days': args.get('rebalance_days', 3),  # 3日调仓
            'stop_loss': args.get('stop_loss', -0.08),  # -8%止损
            'take_profit': args.get('take_profit', 0.50),  # 50%止盈
        }
        
        # 优先使用快速优化版
        try:
            from research.tenbagger_10x_strategy.scripts.tenbagger_fast_optimize import vectorized_backtest, authenticate_jqdata
            import jqdatasdk as jq
            from datetime import datetime, timedelta
            
            if authenticate_jqdata():
                stocks = jq.get_index_stocks('399006.XSHE')[:50]
                stocks += jq.get_index_stocks('000905.XSHG')[:30]
                stocks = list(set(stocks))
                
                price_data = jq.get_price(
                    stocks,
                    start_date=(datetime.strptime(args['start_date'], '%Y-%m-%d') - timedelta(days=30)).strftime('%Y-%m-%d'),
                    end_date=args['end_date'],
                    frequency='daily',
                    fields=['close'],
                    panel=False,
                    skip_paused=True
                )
                
                results = vectorized_backtest(price_data, config)
                jq.logout()
                
                return {
                    "success": True,
                    "metrics": results['metrics'],
                    "trade_count": len(results.get('trades', [])),
                    "config": config
                }
        except Exception as e:
            logger.warning(f"快速回测失败，回退到原版: {e}")
        
        # 回退到原版
        system = _get_system(config)
        results = system.run_backtest(
            start_date=args['start_date'],
            end_date=args['end_date'],
            initial_capital=args.get('initial_capital', 1000000)
        )
        
        if results['success']:
            return {
                "success": True,
                "metrics": results['metrics'],
                "trade_count": results.get('trade_count', 0)
            }
        else:
            return results
            
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_optimize(args: Dict) -> Dict:
    """参数优化"""
    try:
        start_date = args['start_date']
        end_date = args['end_date']
        param_grid = args.get('param_grid', {
            'max_holdings': [3, 5],
            'stop_loss': [-0.08, -0.10, -0.12],
            'take_profit': [0.30, 0.50, 0.80]
        })
        
        best_result = None
        best_sharpe = -float('inf')
        all_results = []
        
        # 网格搜索
        from itertools import product
        
        keys = list(param_grid.keys())
        values = list(param_grid.values())
        
        for combo in product(*values):
            config = dict(zip(keys, combo))
            
            system = _get_system(config)
            result = system.run_backtest(start_date, end_date)
            
            if result['success']:
                sharpe = result['metrics'].get('sharpe_ratio', 0)
                all_results.append({
                    'params': config,
                    'sharpe': sharpe,
                    'total_return': result['metrics'].get('total_return', 0),
                    'max_drawdown': result['metrics'].get('max_drawdown', 0)
                })
                
                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best_result = {
                        'params': config,
                        'metrics': result['metrics']
                    }
        
        return {
            "success": True,
            "best_params": best_result['params'] if best_result else {},
            "best_metrics": best_result['metrics'] if best_result else {},
            "all_results": sorted(all_results, key=lambda x: x['sharpe'], reverse=True)[:10]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_report(args: Dict) -> Dict:
    """生成报告"""
    try:
        scan_date = args.get('scan_date')
        backtest_start = args.get('backtest_start', '2024-01-01')
        backtest_end = args.get('backtest_end', '2025-12-20')
        
        system = _get_system()
        
        # 扫描
        scan_results = system.scan_and_score(scan_date)
        
        # 回测
        backtest_results = system.run_backtest(backtest_start, backtest_end)
        
        # 生成报告
        html = system.generate_report(scan_results, backtest_results)
        
        # 保存
        from datetime import datetime
        reports_dir = PROJECT_ROOT / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"tenbagger_multifactor_{timestamp}.html"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return {
            "success": True,
            "report_path": str(report_path),
            "metrics": backtest_results.get('metrics', {}),
            "top_candidates": [
                {"symbol": r['symbol'], "name": r['name'], "score": r['total_score']}
                for r in system.get_top_candidates(scan_results, 5)
            ]
        }
        
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
async def handle_signal(args: Dict) -> Dict:
    """生成交易信号"""
    try:
        from research.tenbagger_10x_strategy.scripts.tenbagger_signal_generator import TenbaggerSignalGenerator, SignalConfig
        from dataclasses import asdict
        
        config = SignalConfig(
            min_momentum=args.get('min_momentum', 5)
        )
        
        generator = TenbaggerSignalGenerator(config)
        signals = generator.generate_buy_signals(args.get('date'))
        
        return {
            "success": True,
            "date": args.get('date', 'today'),
            "signal_count": len(signals),
            "signals": [asdict(s) for s in signals]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


async def handle_validate(args: Dict) -> Dict:
    """样本外验证"""
    try:
        from research.tenbagger_10x_strategy.scripts.tenbagger_signal_generator import TenbaggerSignalGenerator
        
        generator = TenbaggerSignalGenerator()
        result = generator.validate_out_of_sample(
            train_end=args['train_end'],
            test_start=args['test_start'],
            test_end=args['test_end']
        )
        
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================
# 处理函数映射
# ============================================================

TENBAGGER_MULTIFACTOR_HANDLERS = {
    "tenbagger.multifactor.scan": handle_scan,
    "tenbagger.multifactor.score": handle_score,
    "tenbagger.multifactor.stage": handle_stage,
    "tenbagger.multifactor.backtest": handle_backtest,
    "tenbagger.multifactor.optimize": handle_optimize,
    "tenbagger.multifactor.report": handle_report,
    "tenbagger.multifactor.signal": handle_signal,
    "tenbagger.multifactor.validate": handle_validate,
}


# ============================================================
# 导出
# ============================================================

def get_tools():
    """获取工具列表"""
    return TENBAGGER_MULTIFACTOR_TOOLS


def get_handlers():
    """获取处理函数"""
    return TENBAGGER_MULTIFACTOR_HANDLERS


async def call_tool(name: str, args: Dict) -> Dict:
    """调用工具"""
    handler = TENBAGGER_MULTIFACTOR_HANDLERS.get(name)
    if handler:
        return await handler(args)
    return {"success": False, "error": f"Unknown tool: {name}"}

