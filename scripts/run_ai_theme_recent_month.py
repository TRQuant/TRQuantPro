#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AI主题股票 - 近一个月回测
==========================

使用固定AI主题股票，回测最近一个月表现
使用VBTBacktestV5专业回测引擎（华泰证券标准）

作者: TRQuant Team
日期: 2026-01-12
"""

import sys
sys.path.insert(0, "/home/taotao/.cursor/worktrees/TRQuant/ope")

import json
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
import pandas as pd
import numpy as np

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

# JQData认证
import jqdatasdk as jq
with open("/home/taotao/.cursor/worktrees/TRQuant/ope/config/jqdata_config.json") as f:
    config = json.load(f)
jq.auth(config['username'], config['password'])
logger.info("✅ JQData认证成功")


# ============== AI主题核心股票 ==============

AI_THEME_STOCKS = [
    "002230.XSHE",  # 科大讯飞
    "688111.XSHG",  # 金山办公
    "300058.XSHE",  # 蓝色光标
    "300418.XSHE",  # 昆仑万维
    "300071.XSHE",  # 福石控股
    "603598.XSHG",  # 引力传媒
    "300253.XSHE",  # 卫宁健康
    "600570.XSHG",  # 恒生电子
    "300033.XSHE",  # 同花顺
    "600588.XSHG",  # 用友网络
    "300624.XSHE",  # 万兴科技
    "300229.XSHE",  # 拓尔思
    "300459.XSHE",  # 汤姆猫
    "002405.XSHE",  # 四维图新
    "300496.XSHE",  # 中科创达
]


# ============== 数据构建 ==============

def build_data_matrices(
    stocks: List[str],
    start_date: str,
    end_date: str,
) -> Optional['DataMatrices']:
    """
    构建DataMatrices数据结构
    
    Args:
        stocks: 股票列表
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        DataMatrices或None
    """
    from core.research.data_provider import DataMatrices
    
    logger.info(f"  获取数据: {start_date} ~ {end_date}, {len(stocks)}只股票")
    
    try:
        # 获取价格数据
        price_df = jq.get_price(
            stocks,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume'],
            panel=False,
            skip_paused=True,
        )
        
        if price_df is None or price_df.empty:
            logger.warning("  无法获取价格数据")
            return None
        
        # 转换为矩阵格式
        close = price_df.pivot(index='time', columns='code', values='close')
        open_ = price_df.pivot(index='time', columns='code', values='open')
        high = price_df.pivot(index='time', columns='code', values='high')
        low = price_df.pivot(index='time', columns='code', values='low')
        volume = price_df.pivot(index='time', columns='code', values='volume')
        
        # 过滤有效股票（至少有50%数据的）
        valid_ratio = close.notna().sum() / len(close)
        valid_stocks = valid_ratio[valid_ratio > 0.5].index.tolist()
        
        if not valid_stocks:
            logger.warning("  无有效股票")
            return None
        
        # 过滤并填充缺失值
        close = close[valid_stocks].ffill().bfill()
        open_ = open_[valid_stocks].ffill().bfill()
        high = high[valid_stocks].ffill().bfill()
        low = low[valid_stocks].ffill().bfill()
        volume = volume[valid_stocks].fillna(0)
        
        # 构建is_tradeable（简化：非停牌即可交易）
        is_tradeable = volume > 0
        
        data = DataMatrices(
            close=close,
            open=open_,
            high=high,
            low=low,
            volume=volume,
            is_tradeable=is_tradeable,
        )
        
        logger.info(f"  ✅ 数据构建完成: {data.shape}, 有效股票={len(valid_stocks)}只")
        return data
        
    except Exception as e:
        logger.error(f"  ❌ 数据获取失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def build_signals_from_stocks(
    data: 'DataMatrices',
    selected_stocks: List[str],
    rebalance_freq: int = 5,
) -> Optional['SignalMatrices']:
    """
    基于选中股票构建信号矩阵
    
    Args:
        data: 数据矩阵
        selected_stocks: 选中的股票
        rebalance_freq: 调仓频率（交易日数）
    
    Returns:
        SignalMatrices或None
    """
    from core.research.signals import SignalMatrices
    
    try:
        dates = data.dates
        symbols = data.symbols
        n_dates = len(dates)
        
        # 初始化矩阵
        entries = pd.DataFrame(False, index=dates, columns=symbols)
        exits = pd.DataFrame(False, index=dates, columns=symbols)
        scores = pd.DataFrame(0.0, index=dates, columns=symbols)
        target_weights = pd.DataFrame(0.0, index=dates, columns=symbols)
        
        # 设置调仓日
        rebalance_dates = [dates[i] for i in range(0, n_dates, rebalance_freq)]
        rebalance_mask = pd.Series(False, index=dates)
        rebalance_mask[rebalance_dates] = True
        
        # 过滤有效选中股票
        valid_selected = [s for s in selected_stocks if s in symbols]
        
        if not valid_selected:
            logger.warning("  无有效选中股票")
            return None
        
        # 在调仓日设置信号
        for date in rebalance_dates:
            entries.loc[date, valid_selected] = True
            
            # 等权重
            weight = 1.0 / len(valid_selected)
            target_weights.loc[date, valid_selected] = weight
            
            # 评分（使用当日收益率作为评分的一部分）
            for stock in valid_selected:
                scores.loc[date, stock] = 100.0  # 固定高分
        
        signals = SignalMatrices(
            entries=entries,
            exits=exits,
            scores=scores,
            target_weights=target_weights,
            rebalance_mask=rebalance_mask,
        )
        
        logger.info(f"  ✅ 信号构建完成: 调仓日={len(rebalance_dates)}, 选中股票={len(valid_selected)}")
        return signals
        
    except Exception as e:
        logger.error(f"  ❌ 信号构建失败: {e}")
        import traceback
        traceback.print_exc()
        return None


# ============== 回测函数 ==============

def run_recent_month_backtest(
    start_date: str,
    end_date: str,
    stocks: List[str],
) -> Dict:
    """
    运行近一个月回测
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        stocks: 股票列表
    
    Returns:
        回测结果字典
    """
    from core.research.vbt_backtest_v5 import VBTBacktestV5
    from core.research.signals import SignalParams
    
    result = {
        "start_date": start_date,
        "end_date": end_date,
        "total_return": 0.0,
        "weekly_return": 0.0,
        "annual_return": 0.0,
        "max_drawdown": 0.0,
        "sharpe_ratio": 0.0,
        "win_rate": 0.0,
        "total_trades": 0,
        "selected_stocks": [],
        "trading_days": 0,
        "error": None,
    }
    
    logger.info(f"\n{'='*60}")
    logger.info(f"近一个月回测: {start_date} ~ {end_date}")
    logger.info(f"{'='*60}")
    
    try:
        # 1. 构建数据矩阵
        logger.info("  [1/4] 构建数据矩阵...")
        start_time = time.time()
        
        data = build_data_matrices(stocks, start_date, end_date)
        if data is None:
            result["error"] = "数据获取失败"
            return result
        
        result["trading_days"] = len(data.dates)
        logger.info(f"  耗时: {time.time()-start_time:.1f}s")
        
        # 2. 使用全部有效股票
        logger.info("  [2/4] 选股...")
        start_time = time.time()
        
        selected_stocks = data.symbols
        result["selected_stocks"] = selected_stocks
        result["total_trades"] = len(selected_stocks)
        
        logger.info(f"  选中股票: {len(selected_stocks)}只")
        logger.info(f"  耗时: {time.time()-start_time:.1f}s")
        
        # 3. 构建信号矩阵
        logger.info("  [3/4] 构建信号矩阵...")
        start_time = time.time()
        
        signals = build_signals_from_stocks(
            data=data,
            selected_stocks=selected_stocks,
            rebalance_freq=5,  # 周频调仓
        )
        
        if signals is None:
            result["error"] = "信号构建失败"
            return result
        
        logger.info(f"  耗时: {time.time()-start_time:.1f}s")
        
        # 4. 运行VBTBacktestV5
        logger.info("  [4/4] 运行VBTBacktestV5专业回测...")
        start_time = time.time()
        
        # 配置信号参数
        params = SignalParams(
            max_positions=len(selected_stocks),
            single_position_max=1.0 / len(selected_stocks),  # 等权重
            rebalance_period=5,
            stop_loss_pct=-0.08,
            take_profit_pct=0.30,
            trailing_stop_pct=-0.09,
            trailing_stop_trigger=0.15,
        )
        
        # 创建回测引擎（华泰证券标准）
        backtest = VBTBacktestV5(
            initial_cash=1_000_000,
            commission_rate=0.0001,  # 佣金: 0.01%
            stamp_duty=0.001,  # 印花税: 0.1%
            slippage=0.001,  # 滑点: 0.1%
            transfer_fee_rate=0.00001,  # 过户费: 0.001%
            regulatory_fee_rate=0.0000687,  # 监管费: 0.00687%
            min_commission=5.0,  # 最低佣金: 5元
        )
        
        # 运行回测
        backtest_result = backtest.run_with_signals(
            data=data,
            signals=signals,
            params=params,
        )
        
        logger.info(f"  耗时: {time.time()-start_time:.1f}s")
        
        # 提取结果
        result["total_return"] = backtest_result.total_return
        result["annual_return"] = backtest_result.annual_return
        result["max_drawdown"] = backtest_result.max_drawdown
        result["sharpe_ratio"] = backtest_result.sharpe_ratio
        result["win_rate"] = backtest_result.win_rate
        
        # 计算周收益率
        weeks = result["trading_days"] / 5
        if weeks > 0:
            result["weekly_return"] = ((1 + result["total_return"]/100) ** (1/weeks) - 1) * 100
        else:
            result["weekly_return"] = result["total_return"]
        
        logger.info(f"  ✅ 回测完成!")
        logger.info(f"      总收益: {result['total_return']:.2f}%")
        logger.info(f"      周收益: {result['weekly_return']:.2f}%")
        logger.info(f"      年化: {result['annual_return']:.2f}%")
        logger.info(f"      夏普比: {result['sharpe_ratio']:.2f}")
        logger.info(f"      最大回撤: {result['max_drawdown']:.2f}%")
        logger.info(f"      胜率: {result['win_rate']:.2f}%")
        
    except Exception as e:
        logger.error(f"  ❌ 回测失败: {e}")
        import traceback
        traceback.print_exc()
        result["error"] = str(e)
    
    return result


# ============== 详细报告生成 ==============

def generate_detailed_report(
    result: Dict,
    stocks: List[str],
    start_date: str,
    end_date: str,
) -> str:
    """
    生成详细回测报告
    
    Args:
        result: 回测结果
        stocks: 股票列表
        start_date: 开始日期
        end_date: 结束日期
    
    Returns:
        报告内容（Markdown格式）
    """
    report = []
    
    report.append("# AI主题股票 - 近一个月回测详细报告\n")
    report.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append(f"**回测引擎**: VBTBacktestV5 (华泰证券标准)\n")
    report.append(f"**回测期间**: {start_date} ~ {end_date}\n")
    report.append(f"**交易天数**: {result.get('trading_days', 0)}天\n\n")
    
    # 1. 回测参数
    report.append("## 1. 回测参数\n\n")
    report.append("### 1.1 交易成本（华泰证券标准）\n\n")
    report.append("| 参数 | 值 | 说明 |\n")
    report.append("|------|----|------|\n")
    report.append("| 初始资金 | 100万 | - |\n")
    report.append("| 佣金率 | 0.01% | 买卖双向 |\n")
    report.append("| 印花税 | 0.1% | 仅卖出 |\n")
    report.append("| 过户费 | 0.001% | 买卖双向 |\n")
    report.append("| 监管费 | 0.00687% | 买卖双向 |\n")
    report.append("| 滑点 | 0.1% | - |\n")
    report.append("| 最低佣金 | 5元 | 单笔最低 |\n\n")
    
    report.append("### 1.2 策略参数\n\n")
    report.append("| 参数 | 值 |\n")
    report.append("|------|----|\n")
    report.append("| 选股方式 | 固定AI主题股票 |\n")
    report.append("| 持仓数量 | 等权重组合 |\n")
    report.append("| 调仓频率 | 周频（5个交易日） |\n")
    report.append("| 止损 | -8% |\n")
    report.append("| 止盈 | +30% |\n")
    report.append("| 移动止损 | -9%（盈利15%后启用）|\n\n")
    
    # 2. 股票池
    report.append("## 2. 股票池\n\n")
    report.append(f"**股票数量**: {len(stocks)}只\n\n")
    report.append("| 序号 | 股票代码 | 股票名称 |\n")
    report.append("|------|----------|----------|\n")
    
    # 获取股票名称
    try:
        stock_info = jq.get_all_securities(types=['stock'], date=end_date)
        for i, code in enumerate(stocks, 1):
            display_name = stock_info.loc[code, 'display_name'] if code in stock_info.index else code
            report.append(f"| {i} | {code} | {display_name} |\n")
    except:
        for i, code in enumerate(stocks, 1):
            report.append(f"| {i} | {code} | - |\n")
    
    report.append("\n")
    
    # 3. 回测结果
    report.append("## 3. 回测结果\n\n")
    
    if result.get("error"):
        report.append(f"**❌ 回测失败**: {result['error']}\n\n")
    else:
        report.append("### 3.1 核心指标\n\n")
        report.append("| 指标 | 数值 |\n")
        report.append("|------|------|\n")
        report.append(f"| 总收益率 | {result['total_return']:.2f}% |\n")
        report.append(f"| 周收益率 | {result['weekly_return']:.2f}% |\n")
        report.append(f"| 年化收益率 | {result['annual_return']:.2f}% |\n")
        report.append(f"| 夏普比率 | {result['sharpe_ratio']:.2f} |\n")
        report.append(f"| 最大回撤 | {result['max_drawdown']:.2f}% |\n")
        report.append(f"| 胜率 | {result['win_rate']:.2f}% |\n")
        report.append(f"| 交易天数 | {result.get('trading_days', 0)}天 |\n")
        report.append(f"| 持仓股票数 | {result.get('total_trades', 0)}只 |\n\n")
        
        # 3.2 收益分析
        report.append("### 3.2 收益分析\n\n")
        
        if result['total_return'] > 0:
            report.append(f"✅ **策略表现**: 近一个月实现**{result['total_return']:.2f}%**的正收益\n\n")
        else:
            report.append(f"⚠️ **策略表现**: 近一个月出现**{result['total_return']:.2f}%**的亏损\n\n")
        
        if result['weekly_return'] > 0:
            report.append(f"✅ **周收益**: 平均每周收益**{result['weekly_return']:.2f}%**\n\n")
        else:
            report.append(f"⚠️ **周收益**: 平均每周亏损**{abs(result['weekly_return']):.2f}%**\n\n")
        
        # 3.3 风险分析
        report.append("### 3.3 风险分析\n\n")
        
        if result['max_drawdown'] < 10:
            report.append(f"✅ **回撤控制**: 最大回撤**{result['max_drawdown']:.2f}%**，风险控制良好\n\n")
        elif result['max_drawdown'] < 20:
            report.append(f"⚠️ **回撤控制**: 最大回撤**{result['max_drawdown']:.2f}%**，风险可控\n\n")
        else:
            report.append(f"❌ **回撤控制**: 最大回撤**{result['max_drawdown']:.2f}%**，风险较高\n\n")
        
        if result['sharpe_ratio'] > 2:
            report.append(f"✅ **风险调整收益**: 夏普比率**{result['sharpe_ratio']:.2f}**，表现优秀\n\n")
        elif result['sharpe_ratio'] > 1:
            report.append(f"⚠️ **风险调整收益**: 夏普比率**{result['sharpe_ratio']:.2f}**，表现一般\n\n")
        else:
            report.append(f"❌ **风险调整收益**: 夏普比率**{result['sharpe_ratio']:.2f}**，表现较差\n\n")
        
        # 3.4 交易分析
        report.append("### 3.4 交易分析\n\n")
        report.append(f"- **持仓股票数**: {result.get('total_trades', 0)}只\n")
        report.append(f"- **交易天数**: {result.get('trading_days', 0)}天\n")
        report.append(f"- **调仓频率**: 周频（每5个交易日）\n")
        report.append(f"- **胜率**: {result['win_rate']:.2f}%\n\n")
        
        # 3.5 结论与建议
        report.append("## 4. 结论与建议\n\n")
        
        if result['total_return'] > 10:
            report.append("### 4.1 策略表现\n\n")
            report.append("✅ **策略表现优秀**: 近一个月实现超过10%的收益，表现突出。\n\n")
        elif result['total_return'] > 0:
            report.append("### 4.1 策略表现\n\n")
            report.append("⚠️ **策略表现一般**: 近一个月实现正收益，但收益有限。\n\n")
        else:
            report.append("### 4.1 策略表现\n\n")
            report.append("❌ **策略表现较差**: 近一个月出现亏损，需要优化。\n\n")
        
        report.append("### 4.2 优化建议\n\n")
        
        if result['max_drawdown'] > 20:
            report.append("1. **加强风险控制**: 当前最大回撤较高，建议：\n")
            report.append("   - 降低单只股票仓位上限\n")
            report.append("   - 收紧止损条件\n")
            report.append("   - 增加市场趋势判断\n\n")
        
        if result['sharpe_ratio'] < 1:
            report.append("2. **提升风险调整收益**: 当前夏普比率较低，建议：\n")
            report.append("   - 优化选股逻辑，提高选股质量\n")
            report.append("   - 减少不必要的调仓，降低交易成本\n")
            report.append("   - 结合市场趋势动态调整仓位\n\n")
        
        if result['win_rate'] < 50:
            report.append("3. **提高胜率**: 当前胜率较低，建议：\n")
            report.append("   - 优化买入时机，避免追高\n")
            report.append("   - 加强止损执行，及时止损\n")
            report.append("   - 结合技术指标过滤信号\n\n")
        
        report.append("### 4.3 后续跟踪\n\n")
        report.append("1. **持续监控**: 建议每周跟踪策略表现，及时调整\n")
        report.append("2. **市场环境**: 关注市场趋势变化，适时调整策略参数\n")
        report.append("3. **股票池更新**: 定期评估AI主题股票池，剔除表现不佳的股票\n\n")
    
    return "".join(report)


# ============== 主函数 ==============

def main():
    """主函数"""
    print("="*70)
    print("AI主题股票 - 近一个月回测")
    print("="*70)
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 计算近一个月日期
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    start_date_str = start_date.strftime("%Y-%m-%d")
    end_date_str = end_date.strftime("%Y-%m-%d")
    
    print(f"回测期间: {start_date_str} ~ {end_date_str}")
    print(f"股票数量: {len(AI_THEME_STOCKS)}只")
    print()
    
    # 运行回测
    result = run_recent_month_backtest(
        start_date=start_date_str,
        end_date=end_date_str,
        stocks=AI_THEME_STOCKS,
    )
    
    # 生成详细报告
    report_content = generate_detailed_report(
        result=result,
        stocks=AI_THEME_STOCKS,
        start_date=start_date_str,
        end_date=end_date_str,
    )
    
    # 保存报告
    output_dir = Path("/home/taotao/.cursor/worktrees/TRQuant/ope/output/ai_theme_recent_month")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = output_dir / f"backtest_report_{timestamp}.md"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print("\n" + "="*70)
    print("回测完成")
    print("="*70)
    
    if result.get("error"):
        print(f"❌ 回测失败: {result['error']}")
    else:
        print(f"✅ 总收益: {result['total_return']:.2f}%")
        print(f"✅ 周收益: {result['weekly_return']:.2f}%")
        print(f"✅ 年化: {result['annual_return']:.2f}%")
        print(f"✅ 夏普比: {result['sharpe_ratio']:.2f}")
        print(f"✅ 最大回撤: {result['max_drawdown']:.2f}%")
        print(f"✅ 胜率: {result['win_rate']:.2f}%")
    
    print(f"\n详细报告已保存: {report_path}")
    print(f"完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return result


if __name__ == "__main__":
    main()
