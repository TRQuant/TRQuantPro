#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
整合回测脚本 - MCP工具 + 直接调用结合
=====================================

效率优先原则：
1. MCP工具：用于快速验证和交互
2. 直接调用：用于批量处理和深度分析

调用方式：
1. 命令行：python run_integrated_backtest.py
2. MCP工具：backtest.enhanced, backtest.tenbagger
3. 直接导入：from core.backtest import quick_enhanced_backtest

代码位置: research/tenbagger_10x_strategy/scripts/run_integrated_backtest.py
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import logging
import argparse

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_via_mcp_tool(mode: str = "enhanced", **kwargs):
    """
    通过MCP工具运行回测
    
    适用场景：
    - 快速验证策略
    - 交互式开发
    - 集成到工作流
    """
    logger.info(f"🔧 通过MCP工具运行回测 (mode={mode})")
    
    from core.backtest.enhanced_backtest import (
        mcp_backtest_fast,
        mcp_backtest_enhanced,
        mcp_backtest_precise
    )
    
    if mode == "fast":
        result = mcp_backtest_fast(**kwargs)
    elif mode == "enhanced":
        result = mcp_backtest_enhanced(**kwargs)
    elif mode == "precise":
        result = mcp_backtest_precise(**kwargs)
    else:
        logger.error(f"未知模式: {mode}")
        return None
    
    return result


def run_via_direct_call(mode: str = "enhanced", **kwargs):
    """
    通过直接调用运行回测
    
    适用场景：
    - 批量处理
    - 参数优化
    - 深度分析
    """
    logger.info(f"⚡ 通过直接调用运行回测 (mode={mode})")
    
    from core.backtest.enhanced_backtest import (
        EnhancedBacktestEngine,
        EnhancedBacktestConfig,
        quick_enhanced_backtest,
        batch_enhanced_backtest
    )
    
    if mode == "quick":
        # 快速增强回测
        result = quick_enhanced_backtest(**kwargs)
        return result.to_dict()
    
    elif mode == "batch":
        # 批量回测
        tasks = kwargs.get('tasks', [])
        results = batch_enhanced_backtest(tasks)
        return [r.to_dict() for r in results]
    
    else:
        # 自定义配置
        config = EnhancedBacktestConfig(**kwargs)
        engine = EnhancedBacktestEngine(config)
        
        if mode == "fast":
            result = engine.run_fast()
        elif mode == "standard":
            result = engine.run_standard()
        elif mode == "precise":
            result = engine.run_precise(
                strategy_code=kwargs.get('strategy_code', ''),
                engine=kwargs.get('engine', 'bullettrade')
            )
        elif mode == "enhanced":
            result = engine.run_enhanced()
        else:
            logger.error(f"未知模式: {mode}")
            return None
        
        return result.to_dict()


def run_tenbagger_strategy(**kwargs):
    """
    运行十倍股策略回测
    
    整合因子分析、机器学习和完整指标
    """
    logger.info("🚀 运行十倍股策略回测")
    
    import jqdatasdk as jq
    from core.backtest.enhanced_backtest import (
        EnhancedBacktestEngine,
        EnhancedBacktestConfig
    )
    
    # 默认参数
    start_date = kwargs.get('start_date', '2024-01-01')
    end_date = kwargs.get('end_date', '2025-12-20')
    initial_capital = kwargs.get('initial_capital', 1000000)
    max_holdings = kwargs.get('max_holdings', 5)
    stop_loss = kwargs.get('stop_loss', -0.15)
    take_profit = kwargs.get('take_profit', 1.5)
    
    # 配置
    config = EnhancedBacktestConfig(
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        commission_rate=0.0001,  # 万一佣金
        max_holdings=max_holdings,
        stop_loss=stop_loss,
        take_profit=take_profit,
        enable_factor_analysis=True,
        enable_ml=True
    )
    
    engine = EnhancedBacktestEngine(config)
    
    # 认证
    if not engine.authenticate_jqdata():
        return {"success": False, "error": "JQData认证失败"}
    
    # 获取股票池
    try:
        securities = jq.get_index_stocks('000905.XSHG')  # 中证500
        securities += jq.get_index_stocks('399006.XSHE')[:100]  # 创业板前100
        securities = list(set(securities))
        config.securities = securities
        logger.info(f"   股票池: {len(securities)}只")
    except Exception as e:
        return {"success": False, "error": f"获取股票池失败: {e}"}
    
    # 运行增强回测
    result = engine.run_enhanced()
    
    # 生成报告
    report = {
        "success": result.success,
        "strategy": "十倍股多因子策略",
        "parameters": {
            "start_date": start_date,
            "end_date": end_date,
            "initial_capital": initial_capital,
            "max_holdings": max_holdings,
            "stop_loss": f"{stop_loss*100:.0f}%",
            "take_profit": f"{take_profit*100:.0f}%",
            "stock_pool_size": len(securities)
        },
        "metrics": {
            "total_return": f"{result.total_return*100:.2f}%",
            "annual_return": f"{result.annual_return*100:.2f}%",
            "sharpe_ratio": round(result.sharpe_ratio, 2),
            "sortino_ratio": round(result.sortino_ratio, 2),
            "calmar_ratio": round(result.calmar_ratio, 2),
            "max_drawdown": f"{result.max_drawdown*100:.2f}%",
            "volatility": f"{result.volatility*100:.2f}%",
            "win_rate": f"{result.win_rate*100:.1f}%"
        },
        "duration_seconds": round(result.duration_seconds, 2),
        "factor_analysis": result.factor_analysis,
        "ml_model_info": result.ml_model_info
    }
    
    jq.logout()
    
    return report


def compare_call_methods():
    """
    对比MCP工具和直接调用的效率
    """
    import time
    
    logger.info("=" * 80)
    logger.info("对比MCP工具和直接调用的效率")
    logger.info("=" * 80)
    
    # 测试参数
    params = {
        "securities": ["000001.XSHE", "600000.XSHG", "000002.XSHE"],
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "initial_capital": 1000000
    }
    
    # 1. MCP工具调用
    logger.info("\n1. MCP工具调用...")
    start = time.time()
    mcp_result = run_via_mcp_tool(mode="enhanced", **params)
    mcp_time = time.time() - start
    logger.info(f"   耗时: {mcp_time:.2f}秒")
    
    # 2. 直接调用
    logger.info("\n2. 直接调用...")
    start = time.time()
    direct_result = run_via_direct_call(mode="enhanced", **params)
    direct_time = time.time() - start
    logger.info(f"   耗时: {direct_time:.2f}秒")
    
    # 对比结果
    logger.info("\n" + "=" * 80)
    logger.info("效率对比:")
    logger.info(f"   MCP工具: {mcp_time:.2f}秒")
    logger.info(f"   直接调用: {direct_time:.2f}秒")
    logger.info(f"   效率差异: {abs(mcp_time - direct_time):.2f}秒")
    logger.info("=" * 80)
    
    return {
        "mcp_time": mcp_time,
        "direct_time": direct_time,
        "mcp_result": mcp_result,
        "direct_result": direct_result
    }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='整合回测脚本')
    parser.add_argument('--mode', choices=['mcp', 'direct', 'tenbagger', 'compare'], 
                       default='tenbagger', help='运行模式')
    parser.add_argument('--start', default='2024-01-01', help='开始日期')
    parser.add_argument('--end', default='2025-12-20', help='结束日期')
    parser.add_argument('--capital', type=float, default=1000000, help='初始资金')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("整合回测脚本 - MCP工具 + 直接调用结合")
    print("=" * 80)
    
    if args.mode == 'mcp':
        # 通过MCP工具运行
        result = run_via_mcp_tool(
            mode="enhanced",
            securities=["000001.XSHE", "600000.XSHG"],
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'direct':
        # 通过直接调用运行
        result = run_via_direct_call(
            mode="enhanced",
            securities=["000001.XSHE", "600000.XSHG"],
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'tenbagger':
        # 运行十倍股策略
        result = run_tenbagger_strategy(
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'compare':
        # 对比两种调用方式
        compare_call_methods()
    
    print("=" * 80)
    print("✅ 完成!")
    print("=" * 80)


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
整合回测脚本 - MCP工具 + 直接调用结合
=====================================

效率优先原则：
1. MCP工具：用于快速验证和交互
2. 直接调用：用于批量处理和深度分析

调用方式：
1. 命令行：python run_integrated_backtest.py
2. MCP工具：backtest.enhanced, backtest.tenbagger
3. 直接导入：from core.backtest import quick_enhanced_backtest

代码位置: research/tenbagger_10x_strategy/scripts/run_integrated_backtest.py
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import logging
import argparse

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_via_mcp_tool(mode: str = "enhanced", **kwargs):
    """
    通过MCP工具运行回测
    
    适用场景：
    - 快速验证策略
    - 交互式开发
    - 集成到工作流
    """
    logger.info(f"🔧 通过MCP工具运行回测 (mode={mode})")
    
    from core.backtest.enhanced_backtest import (
        mcp_backtest_fast,
        mcp_backtest_enhanced,
        mcp_backtest_precise
    )
    
    if mode == "fast":
        result = mcp_backtest_fast(**kwargs)
    elif mode == "enhanced":
        result = mcp_backtest_enhanced(**kwargs)
    elif mode == "precise":
        result = mcp_backtest_precise(**kwargs)
    else:
        logger.error(f"未知模式: {mode}")
        return None
    
    return result


def run_via_direct_call(mode: str = "enhanced", **kwargs):
    """
    通过直接调用运行回测
    
    适用场景：
    - 批量处理
    - 参数优化
    - 深度分析
    """
    logger.info(f"⚡ 通过直接调用运行回测 (mode={mode})")
    
    from core.backtest.enhanced_backtest import (
        EnhancedBacktestEngine,
        EnhancedBacktestConfig,
        quick_enhanced_backtest,
        batch_enhanced_backtest
    )
    
    if mode == "quick":
        # 快速增强回测
        result = quick_enhanced_backtest(**kwargs)
        return result.to_dict()
    
    elif mode == "batch":
        # 批量回测
        tasks = kwargs.get('tasks', [])
        results = batch_enhanced_backtest(tasks)
        return [r.to_dict() for r in results]
    
    else:
        # 自定义配置
        config = EnhancedBacktestConfig(**kwargs)
        engine = EnhancedBacktestEngine(config)
        
        if mode == "fast":
            result = engine.run_fast()
        elif mode == "standard":
            result = engine.run_standard()
        elif mode == "precise":
            result = engine.run_precise(
                strategy_code=kwargs.get('strategy_code', ''),
                engine=kwargs.get('engine', 'bullettrade')
            )
        elif mode == "enhanced":
            result = engine.run_enhanced()
        else:
            logger.error(f"未知模式: {mode}")
            return None
        
        return result.to_dict()


def run_tenbagger_strategy(**kwargs):
    """
    运行十倍股策略回测
    
    整合因子分析、机器学习和完整指标
    """
    logger.info("🚀 运行十倍股策略回测")
    
    import jqdatasdk as jq
    from core.backtest.enhanced_backtest import (
        EnhancedBacktestEngine,
        EnhancedBacktestConfig
    )
    
    # 默认参数
    start_date = kwargs.get('start_date', '2024-01-01')
    end_date = kwargs.get('end_date', '2025-12-20')
    initial_capital = kwargs.get('initial_capital', 1000000)
    max_holdings = kwargs.get('max_holdings', 5)
    stop_loss = kwargs.get('stop_loss', -0.15)
    take_profit = kwargs.get('take_profit', 1.5)
    
    # 配置
    config = EnhancedBacktestConfig(
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        commission_rate=0.0001,  # 万一佣金
        max_holdings=max_holdings,
        stop_loss=stop_loss,
        take_profit=take_profit,
        enable_factor_analysis=True,
        enable_ml=True
    )
    
    engine = EnhancedBacktestEngine(config)
    
    # 认证
    if not engine.authenticate_jqdata():
        return {"success": False, "error": "JQData认证失败"}
    
    # 获取股票池
    try:
        securities = jq.get_index_stocks('000905.XSHG')  # 中证500
        securities += jq.get_index_stocks('399006.XSHE')[:100]  # 创业板前100
        securities = list(set(securities))
        config.securities = securities
        logger.info(f"   股票池: {len(securities)}只")
    except Exception as e:
        return {"success": False, "error": f"获取股票池失败: {e}"}
    
    # 运行增强回测
    result = engine.run_enhanced()
    
    # 生成报告
    report = {
        "success": result.success,
        "strategy": "十倍股多因子策略",
        "parameters": {
            "start_date": start_date,
            "end_date": end_date,
            "initial_capital": initial_capital,
            "max_holdings": max_holdings,
            "stop_loss": f"{stop_loss*100:.0f}%",
            "take_profit": f"{take_profit*100:.0f}%",
            "stock_pool_size": len(securities)
        },
        "metrics": {
            "total_return": f"{result.total_return*100:.2f}%",
            "annual_return": f"{result.annual_return*100:.2f}%",
            "sharpe_ratio": round(result.sharpe_ratio, 2),
            "sortino_ratio": round(result.sortino_ratio, 2),
            "calmar_ratio": round(result.calmar_ratio, 2),
            "max_drawdown": f"{result.max_drawdown*100:.2f}%",
            "volatility": f"{result.volatility*100:.2f}%",
            "win_rate": f"{result.win_rate*100:.1f}%"
        },
        "duration_seconds": round(result.duration_seconds, 2),
        "factor_analysis": result.factor_analysis,
        "ml_model_info": result.ml_model_info
    }
    
    jq.logout()
    
    return report


def compare_call_methods():
    """
    对比MCP工具和直接调用的效率
    """
    import time
    
    logger.info("=" * 80)
    logger.info("对比MCP工具和直接调用的效率")
    logger.info("=" * 80)
    
    # 测试参数
    params = {
        "securities": ["000001.XSHE", "600000.XSHG", "000002.XSHE"],
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "initial_capital": 1000000
    }
    
    # 1. MCP工具调用
    logger.info("\n1. MCP工具调用...")
    start = time.time()
    mcp_result = run_via_mcp_tool(mode="enhanced", **params)
    mcp_time = time.time() - start
    logger.info(f"   耗时: {mcp_time:.2f}秒")
    
    # 2. 直接调用
    logger.info("\n2. 直接调用...")
    start = time.time()
    direct_result = run_via_direct_call(mode="enhanced", **params)
    direct_time = time.time() - start
    logger.info(f"   耗时: {direct_time:.2f}秒")
    
    # 对比结果
    logger.info("\n" + "=" * 80)
    logger.info("效率对比:")
    logger.info(f"   MCP工具: {mcp_time:.2f}秒")
    logger.info(f"   直接调用: {direct_time:.2f}秒")
    logger.info(f"   效率差异: {abs(mcp_time - direct_time):.2f}秒")
    logger.info("=" * 80)
    
    return {
        "mcp_time": mcp_time,
        "direct_time": direct_time,
        "mcp_result": mcp_result,
        "direct_result": direct_result
    }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='整合回测脚本')
    parser.add_argument('--mode', choices=['mcp', 'direct', 'tenbagger', 'compare'], 
                       default='tenbagger', help='运行模式')
    parser.add_argument('--start', default='2024-01-01', help='开始日期')
    parser.add_argument('--end', default='2025-12-20', help='结束日期')
    parser.add_argument('--capital', type=float, default=1000000, help='初始资金')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("整合回测脚本 - MCP工具 + 直接调用结合")
    print("=" * 80)
    
    if args.mode == 'mcp':
        # 通过MCP工具运行
        result = run_via_mcp_tool(
            mode="enhanced",
            securities=["000001.XSHE", "600000.XSHG"],
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'direct':
        # 通过直接调用运行
        result = run_via_direct_call(
            mode="enhanced",
            securities=["000001.XSHE", "600000.XSHG"],
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'tenbagger':
        # 运行十倍股策略
        result = run_tenbagger_strategy(
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'compare':
        # 对比两种调用方式
        compare_call_methods()
    
    print("=" * 80)
    print("✅ 完成!")
    print("=" * 80)


if __name__ == "__main__":
    main()






















# -*- coding: utf-8 -*-
"""
整合回测脚本 - MCP工具 + 直接调用结合
=====================================

效率优先原则：
1. MCP工具：用于快速验证和交互
2. 直接调用：用于批量处理和深度分析

调用方式：
1. 命令行：python run_integrated_backtest.py
2. MCP工具：backtest.enhanced, backtest.tenbagger
3. 直接导入：from core.backtest import quick_enhanced_backtest

代码位置: research/tenbagger_10x_strategy/scripts/run_integrated_backtest.py
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import logging
import argparse

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_via_mcp_tool(mode: str = "enhanced", **kwargs):
    """
    通过MCP工具运行回测
    
    适用场景：
    - 快速验证策略
    - 交互式开发
    - 集成到工作流
    """
    logger.info(f"🔧 通过MCP工具运行回测 (mode={mode})")
    
    from core.backtest.enhanced_backtest import (
        mcp_backtest_fast,
        mcp_backtest_enhanced,
        mcp_backtest_precise
    )
    
    if mode == "fast":
        result = mcp_backtest_fast(**kwargs)
    elif mode == "enhanced":
        result = mcp_backtest_enhanced(**kwargs)
    elif mode == "precise":
        result = mcp_backtest_precise(**kwargs)
    else:
        logger.error(f"未知模式: {mode}")
        return None
    
    return result


def run_via_direct_call(mode: str = "enhanced", **kwargs):
    """
    通过直接调用运行回测
    
    适用场景：
    - 批量处理
    - 参数优化
    - 深度分析
    """
    logger.info(f"⚡ 通过直接调用运行回测 (mode={mode})")
    
    from core.backtest.enhanced_backtest import (
        EnhancedBacktestEngine,
        EnhancedBacktestConfig,
        quick_enhanced_backtest,
        batch_enhanced_backtest
    )
    
    if mode == "quick":
        # 快速增强回测
        result = quick_enhanced_backtest(**kwargs)
        return result.to_dict()
    
    elif mode == "batch":
        # 批量回测
        tasks = kwargs.get('tasks', [])
        results = batch_enhanced_backtest(tasks)
        return [r.to_dict() for r in results]
    
    else:
        # 自定义配置
        config = EnhancedBacktestConfig(**kwargs)
        engine = EnhancedBacktestEngine(config)
        
        if mode == "fast":
            result = engine.run_fast()
        elif mode == "standard":
            result = engine.run_standard()
        elif mode == "precise":
            result = engine.run_precise(
                strategy_code=kwargs.get('strategy_code', ''),
                engine=kwargs.get('engine', 'bullettrade')
            )
        elif mode == "enhanced":
            result = engine.run_enhanced()
        else:
            logger.error(f"未知模式: {mode}")
            return None
        
        return result.to_dict()


def run_tenbagger_strategy(**kwargs):
    """
    运行十倍股策略回测
    
    整合因子分析、机器学习和完整指标
    """
    logger.info("🚀 运行十倍股策略回测")
    
    import jqdatasdk as jq
    from core.backtest.enhanced_backtest import (
        EnhancedBacktestEngine,
        EnhancedBacktestConfig
    )
    
    # 默认参数
    start_date = kwargs.get('start_date', '2024-01-01')
    end_date = kwargs.get('end_date', '2025-12-20')
    initial_capital = kwargs.get('initial_capital', 1000000)
    max_holdings = kwargs.get('max_holdings', 5)
    stop_loss = kwargs.get('stop_loss', -0.15)
    take_profit = kwargs.get('take_profit', 1.5)
    
    # 配置
    config = EnhancedBacktestConfig(
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        commission_rate=0.0001,  # 万一佣金
        max_holdings=max_holdings,
        stop_loss=stop_loss,
        take_profit=take_profit,
        enable_factor_analysis=True,
        enable_ml=True
    )
    
    engine = EnhancedBacktestEngine(config)
    
    # 认证
    if not engine.authenticate_jqdata():
        return {"success": False, "error": "JQData认证失败"}
    
    # 获取股票池
    try:
        securities = jq.get_index_stocks('000905.XSHG')  # 中证500
        securities += jq.get_index_stocks('399006.XSHE')[:100]  # 创业板前100
        securities = list(set(securities))
        config.securities = securities
        logger.info(f"   股票池: {len(securities)}只")
    except Exception as e:
        return {"success": False, "error": f"获取股票池失败: {e}"}
    
    # 运行增强回测
    result = engine.run_enhanced()
    
    # 生成报告
    report = {
        "success": result.success,
        "strategy": "十倍股多因子策略",
        "parameters": {
            "start_date": start_date,
            "end_date": end_date,
            "initial_capital": initial_capital,
            "max_holdings": max_holdings,
            "stop_loss": f"{stop_loss*100:.0f}%",
            "take_profit": f"{take_profit*100:.0f}%",
            "stock_pool_size": len(securities)
        },
        "metrics": {
            "total_return": f"{result.total_return*100:.2f}%",
            "annual_return": f"{result.annual_return*100:.2f}%",
            "sharpe_ratio": round(result.sharpe_ratio, 2),
            "sortino_ratio": round(result.sortino_ratio, 2),
            "calmar_ratio": round(result.calmar_ratio, 2),
            "max_drawdown": f"{result.max_drawdown*100:.2f}%",
            "volatility": f"{result.volatility*100:.2f}%",
            "win_rate": f"{result.win_rate*100:.1f}%"
        },
        "duration_seconds": round(result.duration_seconds, 2),
        "factor_analysis": result.factor_analysis,
        "ml_model_info": result.ml_model_info
    }
    
    jq.logout()
    
    return report


def compare_call_methods():
    """
    对比MCP工具和直接调用的效率
    """
    import time
    
    logger.info("=" * 80)
    logger.info("对比MCP工具和直接调用的效率")
    logger.info("=" * 80)
    
    # 测试参数
    params = {
        "securities": ["000001.XSHE", "600000.XSHG", "000002.XSHE"],
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "initial_capital": 1000000
    }
    
    # 1. MCP工具调用
    logger.info("\n1. MCP工具调用...")
    start = time.time()
    mcp_result = run_via_mcp_tool(mode="enhanced", **params)
    mcp_time = time.time() - start
    logger.info(f"   耗时: {mcp_time:.2f}秒")
    
    # 2. 直接调用
    logger.info("\n2. 直接调用...")
    start = time.time()
    direct_result = run_via_direct_call(mode="enhanced", **params)
    direct_time = time.time() - start
    logger.info(f"   耗时: {direct_time:.2f}秒")
    
    # 对比结果
    logger.info("\n" + "=" * 80)
    logger.info("效率对比:")
    logger.info(f"   MCP工具: {mcp_time:.2f}秒")
    logger.info(f"   直接调用: {direct_time:.2f}秒")
    logger.info(f"   效率差异: {abs(mcp_time - direct_time):.2f}秒")
    logger.info("=" * 80)
    
    return {
        "mcp_time": mcp_time,
        "direct_time": direct_time,
        "mcp_result": mcp_result,
        "direct_result": direct_result
    }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='整合回测脚本')
    parser.add_argument('--mode', choices=['mcp', 'direct', 'tenbagger', 'compare'], 
                       default='tenbagger', help='运行模式')
    parser.add_argument('--start', default='2024-01-01', help='开始日期')
    parser.add_argument('--end', default='2025-12-20', help='结束日期')
    parser.add_argument('--capital', type=float, default=1000000, help='初始资金')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("整合回测脚本 - MCP工具 + 直接调用结合")
    print("=" * 80)
    
    if args.mode == 'mcp':
        # 通过MCP工具运行
        result = run_via_mcp_tool(
            mode="enhanced",
            securities=["000001.XSHE", "600000.XSHG"],
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'direct':
        # 通过直接调用运行
        result = run_via_direct_call(
            mode="enhanced",
            securities=["000001.XSHE", "600000.XSHG"],
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'tenbagger':
        # 运行十倍股策略
        result = run_tenbagger_strategy(
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'compare':
        # 对比两种调用方式
        compare_call_methods()
    
    print("=" * 80)
    print("✅ 完成!")
    print("=" * 80)


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
整合回测脚本 - MCP工具 + 直接调用结合
=====================================

效率优先原则：
1. MCP工具：用于快速验证和交互
2. 直接调用：用于批量处理和深度分析

调用方式：
1. 命令行：python run_integrated_backtest.py
2. MCP工具：backtest.enhanced, backtest.tenbagger
3. 直接导入：from core.backtest import quick_enhanced_backtest

代码位置: research/tenbagger_10x_strategy/scripts/run_integrated_backtest.py
"""

import sys
from pathlib import Path
from datetime import datetime
import json
import logging
import argparse

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_via_mcp_tool(mode: str = "enhanced", **kwargs):
    """
    通过MCP工具运行回测
    
    适用场景：
    - 快速验证策略
    - 交互式开发
    - 集成到工作流
    """
    logger.info(f"🔧 通过MCP工具运行回测 (mode={mode})")
    
    from core.backtest.enhanced_backtest import (
        mcp_backtest_fast,
        mcp_backtest_enhanced,
        mcp_backtest_precise
    )
    
    if mode == "fast":
        result = mcp_backtest_fast(**kwargs)
    elif mode == "enhanced":
        result = mcp_backtest_enhanced(**kwargs)
    elif mode == "precise":
        result = mcp_backtest_precise(**kwargs)
    else:
        logger.error(f"未知模式: {mode}")
        return None
    
    return result


def run_via_direct_call(mode: str = "enhanced", **kwargs):
    """
    通过直接调用运行回测
    
    适用场景：
    - 批量处理
    - 参数优化
    - 深度分析
    """
    logger.info(f"⚡ 通过直接调用运行回测 (mode={mode})")
    
    from core.backtest.enhanced_backtest import (
        EnhancedBacktestEngine,
        EnhancedBacktestConfig,
        quick_enhanced_backtest,
        batch_enhanced_backtest
    )
    
    if mode == "quick":
        # 快速增强回测
        result = quick_enhanced_backtest(**kwargs)
        return result.to_dict()
    
    elif mode == "batch":
        # 批量回测
        tasks = kwargs.get('tasks', [])
        results = batch_enhanced_backtest(tasks)
        return [r.to_dict() for r in results]
    
    else:
        # 自定义配置
        config = EnhancedBacktestConfig(**kwargs)
        engine = EnhancedBacktestEngine(config)
        
        if mode == "fast":
            result = engine.run_fast()
        elif mode == "standard":
            result = engine.run_standard()
        elif mode == "precise":
            result = engine.run_precise(
                strategy_code=kwargs.get('strategy_code', ''),
                engine=kwargs.get('engine', 'bullettrade')
            )
        elif mode == "enhanced":
            result = engine.run_enhanced()
        else:
            logger.error(f"未知模式: {mode}")
            return None
        
        return result.to_dict()


def run_tenbagger_strategy(**kwargs):
    """
    运行十倍股策略回测
    
    整合因子分析、机器学习和完整指标
    """
    logger.info("🚀 运行十倍股策略回测")
    
    import jqdatasdk as jq
    from core.backtest.enhanced_backtest import (
        EnhancedBacktestEngine,
        EnhancedBacktestConfig
    )
    
    # 默认参数
    start_date = kwargs.get('start_date', '2024-01-01')
    end_date = kwargs.get('end_date', '2025-12-20')
    initial_capital = kwargs.get('initial_capital', 1000000)
    max_holdings = kwargs.get('max_holdings', 5)
    stop_loss = kwargs.get('stop_loss', -0.15)
    take_profit = kwargs.get('take_profit', 1.5)
    
    # 配置
    config = EnhancedBacktestConfig(
        start_date=start_date,
        end_date=end_date,
        initial_capital=initial_capital,
        commission_rate=0.0001,  # 万一佣金
        max_holdings=max_holdings,
        stop_loss=stop_loss,
        take_profit=take_profit,
        enable_factor_analysis=True,
        enable_ml=True
    )
    
    engine = EnhancedBacktestEngine(config)
    
    # 认证
    if not engine.authenticate_jqdata():
        return {"success": False, "error": "JQData认证失败"}
    
    # 获取股票池
    try:
        securities = jq.get_index_stocks('000905.XSHG')  # 中证500
        securities += jq.get_index_stocks('399006.XSHE')[:100]  # 创业板前100
        securities = list(set(securities))
        config.securities = securities
        logger.info(f"   股票池: {len(securities)}只")
    except Exception as e:
        return {"success": False, "error": f"获取股票池失败: {e}"}
    
    # 运行增强回测
    result = engine.run_enhanced()
    
    # 生成报告
    report = {
        "success": result.success,
        "strategy": "十倍股多因子策略",
        "parameters": {
            "start_date": start_date,
            "end_date": end_date,
            "initial_capital": initial_capital,
            "max_holdings": max_holdings,
            "stop_loss": f"{stop_loss*100:.0f}%",
            "take_profit": f"{take_profit*100:.0f}%",
            "stock_pool_size": len(securities)
        },
        "metrics": {
            "total_return": f"{result.total_return*100:.2f}%",
            "annual_return": f"{result.annual_return*100:.2f}%",
            "sharpe_ratio": round(result.sharpe_ratio, 2),
            "sortino_ratio": round(result.sortino_ratio, 2),
            "calmar_ratio": round(result.calmar_ratio, 2),
            "max_drawdown": f"{result.max_drawdown*100:.2f}%",
            "volatility": f"{result.volatility*100:.2f}%",
            "win_rate": f"{result.win_rate*100:.1f}%"
        },
        "duration_seconds": round(result.duration_seconds, 2),
        "factor_analysis": result.factor_analysis,
        "ml_model_info": result.ml_model_info
    }
    
    jq.logout()
    
    return report


def compare_call_methods():
    """
    对比MCP工具和直接调用的效率
    """
    import time
    
    logger.info("=" * 80)
    logger.info("对比MCP工具和直接调用的效率")
    logger.info("=" * 80)
    
    # 测试参数
    params = {
        "securities": ["000001.XSHE", "600000.XSHG", "000002.XSHE"],
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "initial_capital": 1000000
    }
    
    # 1. MCP工具调用
    logger.info("\n1. MCP工具调用...")
    start = time.time()
    mcp_result = run_via_mcp_tool(mode="enhanced", **params)
    mcp_time = time.time() - start
    logger.info(f"   耗时: {mcp_time:.2f}秒")
    
    # 2. 直接调用
    logger.info("\n2. 直接调用...")
    start = time.time()
    direct_result = run_via_direct_call(mode="enhanced", **params)
    direct_time = time.time() - start
    logger.info(f"   耗时: {direct_time:.2f}秒")
    
    # 对比结果
    logger.info("\n" + "=" * 80)
    logger.info("效率对比:")
    logger.info(f"   MCP工具: {mcp_time:.2f}秒")
    logger.info(f"   直接调用: {direct_time:.2f}秒")
    logger.info(f"   效率差异: {abs(mcp_time - direct_time):.2f}秒")
    logger.info("=" * 80)
    
    return {
        "mcp_time": mcp_time,
        "direct_time": direct_time,
        "mcp_result": mcp_result,
        "direct_result": direct_result
    }


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='整合回测脚本')
    parser.add_argument('--mode', choices=['mcp', 'direct', 'tenbagger', 'compare'], 
                       default='tenbagger', help='运行模式')
    parser.add_argument('--start', default='2024-01-01', help='开始日期')
    parser.add_argument('--end', default='2025-12-20', help='结束日期')
    parser.add_argument('--capital', type=float, default=1000000, help='初始资金')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("整合回测脚本 - MCP工具 + 直接调用结合")
    print("=" * 80)
    
    if args.mode == 'mcp':
        # 通过MCP工具运行
        result = run_via_mcp_tool(
            mode="enhanced",
            securities=["000001.XSHE", "600000.XSHG"],
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'direct':
        # 通过直接调用运行
        result = run_via_direct_call(
            mode="enhanced",
            securities=["000001.XSHE", "600000.XSHG"],
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'tenbagger':
        # 运行十倍股策略
        result = run_tenbagger_strategy(
            start_date=args.start,
            end_date=args.end,
            initial_capital=args.capital
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        
    elif args.mode == 'compare':
        # 对比两种调用方式
        compare_call_methods()
    
    print("=" * 80)
    print("✅ 完成!")
    print("=" * 80)


if __name__ == "__main__":
    main()









































