#!/usr/bin/env python3
"""
市场环境信号历史回测验证
========================

验证动态信号在2020-2025年的历史表现
"""

import sys
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_historical_data(jq_client, index_code: str, start_date: str, end_date: str) -> pd.DataFrame:
    """获取历史数据"""
    df = jq_client.get_price(
        index_code, 
        start_date=start_date, 
        end_date=end_date,
        frequency='daily',
        fields=['open', 'high', 'low', 'close', 'volume']
    )
    if df is not None:
        df = df.reset_index()
        df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    return df


def calculate_signal_returns(df: pd.DataFrame, signals_df: pd.DataFrame, holding_period: int = 20) -> pd.DataFrame:
    """计算信号后的收益率"""
    results = []
    
    for idx, row in signals_df.iterrows():
        signal_date = row['date']
        signal_value = row['signal_value']
        
        # 找到信号日期在价格数据中的位置
        try:
            signal_idx = df[df['date'] == signal_date].index[0]
            future_idx = min(signal_idx + holding_period, len(df) - 1)
            
            entry_price = df.loc[signal_idx, 'close']
            exit_price = df.loc[future_idx, 'close']
            
            ret = (exit_price - entry_price) / entry_price * 100
            
            results.append({
                'date': signal_date,
                'signal_value': signal_value,
                'entry_price': entry_price,
                'exit_price': exit_price,
                'return_pct': ret,
                'holding_days': future_idx - signal_idx
            })
        except (IndexError, KeyError):
            continue
    
    return pd.DataFrame(results)


def backtest_trend_signal(jq_client, index_code: str = "000001.XSHG"):
    """回测趋势信号"""
    from core.trend_analyzer import TrendAnalyzer
    
    logger.info("开始趋势信号回测...")
    
    # 获取历史数据
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = "2020-01-01"
    
    df = get_historical_data(jq_client, index_code, start_date, end_date)
    if df is None or len(df) < 100:
        logger.error("数据不足")
        return None
    
    # 计算简化的趋势信号
    df['returns'] = df['close'].pct_change()
    df['ma20'] = df['close'].rolling(20).mean()
    df['ma60'] = df['close'].rolling(60).mean()
    
    # 趋势信号：MA20 > MA60 为正
    df['trend_signal'] = np.where(df['ma20'] > df['ma60'], 1, -1)
    df['signal_change'] = df['trend_signal'].diff()
    
    # 找到信号变化点
    signal_points = df[df['signal_change'] != 0].copy()
    signal_points = signal_points.rename(columns={'trend_signal': 'signal_value'})
    
    # 计算信号后收益
    results = calculate_signal_returns(df, signal_points[['date', 'signal_value']], holding_period=20)
    
    if len(results) > 0:
        # 按信号方向分组统计
        bullish = results[results['signal_value'] > 0]
        bearish = results[results['signal_value'] < 0]
        
        logger.info(f"\n趋势信号回测结果 ({start_date} ~ {end_date}):")
        logger.info(f"  总信号数: {len(results)}")
        logger.info(f"  看涨信号: {len(bullish)}, 平均收益: {bullish['return_pct'].mean():.2f}%")
        logger.info(f"  看跌信号: {len(bearish)}, 平均收益: {bearish['return_pct'].mean():.2f}%")
        
        # 信号有效性：看涨信号后应该上涨，看跌信号后应该下跌
        bullish_accuracy = (bullish['return_pct'] > 0).mean() * 100 if len(bullish) > 0 else 0
        bearish_accuracy = (bearish['return_pct'] < 0).mean() * 100 if len(bearish) > 0 else 0
        
        logger.info(f"  看涨准确率: {bullish_accuracy:.1f}%")
        logger.info(f"  看跌准确率: {bearish_accuracy:.1f}%")
        
        return {
            'total_signals': len(results),
            'bullish_signals': len(bullish),
            'bearish_signals': len(bearish),
            'bullish_avg_return': bullish['return_pct'].mean() if len(bullish) > 0 else 0,
            'bearish_avg_return': bearish['return_pct'].mean() if len(bearish) > 0 else 0,
            'bullish_accuracy': bullish_accuracy,
            'bearish_accuracy': bearish_accuracy
        }
    
    return None


def backtest_ibd_signal(jq_client, index_code: str = "000001.XSHG"):
    """回测IBD信号（简化版）"""
    logger.info("开始IBD信号回测...")
    
    # 获取历史数据
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = "2020-01-01"
    
    df = get_historical_data(jq_client, index_code, start_date, end_date)
    if df is None or len(df) < 100:
        logger.error("数据不足")
        return None
    
    df['returns'] = df['close'].pct_change() * 100
    df['vol_ratio'] = df['volume'] / df['volume'].rolling(20).mean()
    
    # 简化的跟踪日识别：涨幅>1.7%，量比>1.0
    df['ftd'] = ((df['returns'] > 1.7) & (df['vol_ratio'] > 1.0)).astype(int)
    
    # 简化的分布日识别：跌幅>0.2%，量比>1.0
    df['dist'] = ((df['returns'] < -0.2) & (df['vol_ratio'] > 1.0)).astype(int)
    
    # 计算跟踪日后收益
    ftd_dates = df[df['ftd'] == 1][['date']].copy()
    ftd_dates['signal_value'] = 1
    
    if len(ftd_dates) > 0:
        ftd_results = calculate_signal_returns(df, ftd_dates, holding_period=20)
        
        logger.info(f"\nIBD跟踪日回测结果:")
        logger.info(f"  跟踪日数量: {len(ftd_dates)}")
        if len(ftd_results) > 0:
            logger.info(f"  平均20日收益: {ftd_results['return_pct'].mean():.2f}%")
            logger.info(f"  上涨概率: {(ftd_results['return_pct'] > 0).mean()*100:.1f}%")
            
            return {
                'ftd_count': len(ftd_dates),
                'avg_return': ftd_results['return_pct'].mean(),
                'win_rate': (ftd_results['return_pct'] > 0).mean() * 100
            }
    
    return None


def backtest_position_strategy(jq_client, index_code: str = "000001.XSHG"):
    """回测仓位策略"""
    logger.info("开始仓位策略回测...")
    
    # 获取历史数据
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = "2020-01-01"
    
    df = get_historical_data(jq_client, index_code, start_date, end_date)
    if df is None or len(df) < 100:
        logger.error("数据不足")
        return None
    
    df['returns'] = df['close'].pct_change()
    df['ma20'] = df['close'].rolling(20).mean()
    df['ma60'] = df['close'].rolling(60).mean()
    df['volatility'] = df['returns'].rolling(20).std() * np.sqrt(252)
    
    # 简化仓位计算：趋势向上且波动率低时高仓位
    def calc_position(row):
        if pd.isna(row['ma20']) or pd.isna(row['ma60']) or pd.isna(row['volatility']):
            return 0.5
        
        trend_score = 1 if row['ma20'] > row['ma60'] else -1
        vol_score = 1 - min(1, row['volatility'] / 0.3)  # 波动率>30%时为0
        
        position = (trend_score + 1) / 2 * 0.5 + vol_score * 0.5
        return max(0.1, min(1.0, position))
    
    df['position'] = df.apply(calc_position, axis=1)
    
    # 计算策略收益
    df['strategy_returns'] = df['returns'] * df['position'].shift(1)
    df['cumulative_benchmark'] = (1 + df['returns']).cumprod()
    df['cumulative_strategy'] = (1 + df['strategy_returns']).cumprod()
    
    # 计算统计指标
    total_benchmark_return = (df['cumulative_benchmark'].iloc[-1] - 1) * 100
    total_strategy_return = (df['cumulative_strategy'].iloc[-1] - 1) * 100
    
    benchmark_sharpe = df['returns'].mean() / df['returns'].std() * np.sqrt(252) if df['returns'].std() > 0 else 0
    strategy_sharpe = df['strategy_returns'].mean() / df['strategy_returns'].std() * np.sqrt(252) if df['strategy_returns'].std() > 0 else 0
    
    logger.info(f"\n仓位策略回测结果 ({start_date} ~ {end_date}):")
    logger.info(f"  基准总收益: {total_benchmark_return:.2f}%")
    logger.info(f"  策略总收益: {total_strategy_return:.2f}%")
    logger.info(f"  基准夏普: {benchmark_sharpe:.2f}")
    logger.info(f"  策略夏普: {strategy_sharpe:.2f}")
    logger.info(f"  平均仓位: {df['position'].mean():.1%}")
    
    return {
        'benchmark_return': total_benchmark_return,
        'strategy_return': total_strategy_return,
        'benchmark_sharpe': benchmark_sharpe,
        'strategy_sharpe': strategy_sharpe,
        'avg_position': df['position'].mean()
    }


def main():
    """主函数"""
    from notebooks.lib import get_jqdata_client
    
    logger.info("=" * 60)
    logger.info("市场环境信号历史回测")
    logger.info("=" * 60)
    
    jq = get_jqdata_client()
    
    results = {}
    
    # 1. 趋势信号回测
    try:
        results['trend'] = backtest_trend_signal(jq)
    except Exception as e:
        logger.error(f"趋势信号回测失败: {e}")
    
    # 2. IBD信号回测
    try:
        results['ibd'] = backtest_ibd_signal(jq)
    except Exception as e:
        logger.error(f"IBD信号回测失败: {e}")
    
    # 3. 仓位策略回测
    try:
        results['position'] = backtest_position_strategy(jq)
    except Exception as e:
        logger.error(f"仓位策略回测失败: {e}")
    
    # 汇总
    logger.info("\n" + "=" * 60)
    logger.info("回测汇总")
    logger.info("=" * 60)
    
    passed = 0
    total = 0
    
    if results.get('trend'):
        total += 1
        if results['trend']['bullish_accuracy'] > 50:
            passed += 1
            logger.info("✅ 趋势信号: 有效")
        else:
            logger.info("⚠️ 趋势信号: 准确率偏低")
    
    if results.get('ibd'):
        total += 1
        if results['ibd']['win_rate'] > 50:
            passed += 1
            logger.info("✅ IBD信号: 有效")
        else:
            logger.info("⚠️ IBD信号: 胜率偏低")
    
    if results.get('position'):
        total += 1
        if results['position']['strategy_sharpe'] > results['position']['benchmark_sharpe']:
            passed += 1
            logger.info("✅ 仓位策略: 优于基准")
        else:
            logger.info("⚠️ 仓位策略: 未能战胜基准")
    
    logger.info(f"\n总计: {passed}/{total} 项通过")
    
    return results


if __name__ == "__main__":
    main()
