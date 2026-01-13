#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
追涨策略信号有效性分析脚本

Phase 1: 信号统计分析
- 分析训练集数据中各种信号类型的出现频率
- 统计各信号类型的平均收益率和胜率
- 分析信号评分与收益率的相关性

数据集:
- 训练集: 2019-01-01~2020-06-30 + 2024-09-01~2025-06-30
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import pandas as pd
import numpy as np
import logging
import json

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.config_manager import get_config_manager
import jqdatasdk as jq

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ==================== 信号类型定义 ====================

class SignalType:
    """信号类型"""
    FIRST_LIMIT_UP = "FIRST_LIMIT_UP"  # 首板启动
    CONSECUTIVE_LIMIT_UP = "CONSECUTIVE_LIMIT_UP"  # 连板加速
    STRONG_BREAKOUT = "STRONG_BREAKOUT"  # 强势突破
    VOLUME_PRICE_RISE = "VOLUME_PRICE_RISE"  # 量价齐升
    NO_SIGNAL = "NO_SIGNAL"  # 无信号


# ==================== 信号计算函数 ====================

def calculate_chase_rise_signal(
    close: np.ndarray,
    volume: np.ndarray,
    limit_up_threshold: float = 0.095,
    vol_ratio_threshold_first: float = 3.0,
    mom_5d_threshold_breakout: float = 15.0,
    mom_5d_threshold_volume: float = 10.0,
    vol_ratio_threshold_breakout: float = 1.5,
    vol_ratio_threshold_volume: float = 2.0,
) -> Tuple[float, str]:
    """
    计算追涨信号评分和类型
    
    Args:
        close: 收盘价序列
        volume: 成交量序列
        limit_up_threshold: 涨停阈值（默认9.5%）
        vol_ratio_threshold_first: 首板放量阈值（默认3.0倍）
        mom_5d_threshold_breakout: 强势突破5日动量阈值（默认15%）
        mom_5d_threshold_volume: 量价齐升5日动量阈值（默认10%）
        vol_ratio_threshold_breakout: 强势突破量比阈值（默认1.5倍）
        vol_ratio_threshold_volume: 量价齐升量比阈值（默认2.0倍）
    
    Returns:
        Tuple[float, str]: (评分, 信号类型)
    """
    if len(close) < 21:
        return 0.0, SignalType.NO_SIGNAL
    
    score = 0.0
    signal_type = SignalType.NO_SIGNAL
    
    # 计算基础指标
    daily_return = close[-1] / close[-2] - 1 if len(close) >= 2 else 0
    is_limit_up = daily_return > limit_up_threshold
    
    # 近5日涨停计数
    limit_up_recent = 0
    for j in range(max(len(close)-5, 1), len(close)):
        if j > 0 and close[j] / close[j-1] - 1 > limit_up_threshold:
            limit_up_recent += 1
    
    # 5日动量
    mom_5d = (close[-1] / close[-6] - 1) * 100 if len(close) >= 6 else 0
    
    # 量比
    vol_ratio = volume[-1] / np.mean(volume[-20:]) if len(volume) >= 20 and np.mean(volume[-20:]) > 0 else 1.0
    
    # 信号1: 首板启动
    if is_limit_up and limit_up_recent == 1:
        score = 75
        signal_type = SignalType.FIRST_LIMIT_UP
        if vol_ratio > vol_ratio_threshold_first:
            score += 15
        return score, signal_type
    
    # 信号2: 连板加速
    if limit_up_recent >= 2:
        score = 65
        signal_type = SignalType.CONSECUTIVE_LIMIT_UP
        return score, signal_type
    
    # 信号3: 强势突破
    if mom_5d > mom_5d_threshold_breakout and vol_ratio > vol_ratio_threshold_breakout:
        score = 60
        signal_type = SignalType.STRONG_BREAKOUT
        return score, signal_type
    
    # 信号4: 量价齐升
    if mom_5d > mom_5d_threshold_volume and vol_ratio > vol_ratio_threshold_volume:
        score = 55
        signal_type = SignalType.VOLUME_PRICE_RISE
        return score, signal_type
    
    return score, signal_type


def analyze_signals_for_stock(
    jq_client,
    stock_code: str,
    start_date: str,
    end_date: str,
    rebalance_days: int = 5,
    limit_up_threshold: float = 0.095,
    vol_ratio_threshold_first: float = 3.0,
    mom_5d_threshold_breakout: float = 15.0,
    mom_5d_threshold_volume: float = 10.0,
    vol_ratio_threshold_breakout: float = 1.5,
    vol_ratio_threshold_volume: float = 2.0,
) -> List[Dict]:
    """
    分析单只股票在指定时间段内的信号
    
    Returns:
        List[Dict]: 信号记录列表，每个记录包含日期、信号类型、评分、未来收益率
    """
    try:
        # 获取交易日
        trade_days = jq_client.get_trade_days(start_date=start_date, end_date=end_date)
        if trade_days is None or len(trade_days) < 25:
            return []
        
        signals = []
        
        # 在调仓日计算信号
        for i in range(20, len(trade_days), rebalance_days):  # 从第20个交易日开始，每rebalance_days天
            current_date = trade_days[i]
            date_str = current_date.strftime('%Y-%m-%d') if hasattr(current_date, 'strftime') else str(current_date)
            
            # 获取历史数据（获取到当前日期的数据）
            df = jq_client.get_price(
                stock_code,
                end_date=date_str,
                count=65,  # 获取足够的历史数据
                frequency='daily',
                fields=['close', 'volume', 'high', 'low'],
                fq='post'
            )
            
            if df is None or len(df) < 25:
                continue
            
            close = df['close'].values
            volume = df['volume'].values
            
            # 计算信号（使用全部历史数据）
            score, signal_type = calculate_chase_rise_signal(
                close,
                volume,
                limit_up_threshold=limit_up_threshold,
                vol_ratio_threshold_first=vol_ratio_threshold_first,
                mom_5d_threshold_breakout=mom_5d_threshold_breakout,
                mom_5d_threshold_volume=mom_5d_threshold_volume,
                vol_ratio_threshold_breakout=vol_ratio_threshold_breakout,
                vol_ratio_threshold_volume=vol_ratio_threshold_volume,
            )
            
            if signal_type == SignalType.NO_SIGNAL or score < 55:
                continue
            
            # 计算未来收益率（5个交易日）
            future_return = 0.0
            if i + 5 < len(trade_days):
                future_date = trade_days[i + 5]
                future_date_str = future_date.strftime('%Y-%m-%d') if hasattr(future_date, 'strftime') else str(future_date)
                
                # 获取未来价格
                try:
                    future_df = jq_client.get_price(
                        stock_code,
                        end_date=future_date_str,
                        count=1,
                        frequency='daily',
                        fields=['close'],
                        fq='post'
                    )
                    if future_df is not None and len(future_df) > 0:
                        entry_price = close[-1]  # 当前收盘价
                        exit_price = future_df['close'].iloc[-1]
                        future_return = (exit_price / entry_price - 1) * 100
                except:
                    pass
            
            signals.append({
                'code': stock_code,
                'date': date_str,
                'signal_type': signal_type,
                'score': score,
                'entry_price': close[-1],
                'future_return_5d': future_return,
                'is_winning': future_return > 0,
            })
        
        return signals
    
    except Exception as e:
        logger.debug(f"分析{stock_code}失败: {e}")
        return []


def analyze_signals_for_period(
    jq_client,
    start_date: str,
    end_date: str,
    universe: Optional[List[str]] = None,
    max_stocks: int = 300,
    rebalance_days: int = 5,
    **signal_params
) -> pd.DataFrame:
    """
    分析指定时间段内所有股票的信号
    
    Returns:
        pd.DataFrame: 包含所有信号记录的DataFrame
    """
    logger.info(f"开始分析信号: {start_date} ~ {end_date}")
    
    # 获取股票池
    if universe is None:
        try:
            securities = jq_client.get_all_securities(types=['stock'], date=end_date)
            stocks = securities.index.tolist()
            # 过滤ST股票
            universe = [
                code for code in stocks
                if 'ST' not in str(securities.loc[code, 'display_name']).upper()
            ]
            logger.info(f"股票池大小: {len(universe)}")
        except Exception as e:
            logger.error(f"获取股票池失败: {e}")
            return pd.DataFrame()
    
    # 限制股票数量以加速
    if max_stocks > 0:
        universe = universe[:max_stocks]
    
    all_signals = []
    
    for i, stock in enumerate(universe):
        if (i + 1) % 50 == 0:
            logger.info(f"  进度: {i+1}/{len(universe)}")
        
        signals = analyze_signals_for_stock(
            jq_client,
            stock,
            start_date,
            end_date,
            rebalance_days=rebalance_days,
            **signal_params
        )
        all_signals.extend(signals)
    
    if not all_signals:
        logger.warning("未找到任何信号")
        return pd.DataFrame()
    
    df = pd.DataFrame(all_signals)
    logger.info(f"✅ 共找到 {len(df)} 个信号")
    
    return df


def analyze_signal_statistics(df: pd.DataFrame) -> Dict:
    """
    统计分析信号有效性
    
    Returns:
        Dict: 统计结果
    """
    if df.empty:
        return {}
    
    stats = {}
    
    # 按信号类型统计
    for signal_type in df['signal_type'].unique():
        type_df = df[df['signal_type'] == signal_type]
        
        stats[signal_type] = {
            'count': len(type_df),
            'frequency': len(type_df) / len(df) * 100,
            'avg_return': type_df['future_return_5d'].mean(),
            'median_return': type_df['future_return_5d'].median(),
            'win_rate': type_df['is_winning'].sum() / len(type_df) * 100,
            'avg_score': type_df['score'].mean(),
            'max_return': type_df['future_return_5d'].max(),
            'min_return': type_df['future_return_5d'].min(),
        }
    
    # 总体统计
    stats['overall'] = {
        'total_signals': len(df),
        'avg_return': df['future_return_5d'].mean(),
        'median_return': df['future_return_5d'].median(),
        'win_rate': df['is_winning'].sum() / len(df) * 100,
        'avg_score': df['score'].mean(),
    }
    
    # 评分与收益率相关性
    if len(df) > 1:
        correlation = df['score'].corr(df['future_return_5d'])
        stats['correlation'] = {
            'score_vs_return': correlation,
        }
    
    return stats


def main():
    """主函数"""
    logger.info("=" * 70)
    logger.info("追涨策略信号有效性分析")
    logger.info("=" * 70)
    
    # 初始化JQData
    try:
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config('jqdata')
        jq.auth(jq_config['username'], jq_config['password'])
        logger.info("✅ JQData连接成功")
    except Exception as e:
        logger.error(f"❌ JQData连接失败: {e}")
        return
    
    # 数据集划分
    train_periods = [
        ('2019-01-01', '2020-06-30'),
        ('2024-09-01', '2025-06-30'),
    ]
    
    # 信号参数（使用当前默认值）
    signal_params = {
        'limit_up_threshold': 0.095,
        'vol_ratio_threshold_first': 3.0,
        'mom_5d_threshold_breakout': 15.0,
        'mom_5d_threshold_volume': 10.0,
        'vol_ratio_threshold_breakout': 1.5,
        'vol_ratio_threshold_volume': 2.0,
    }
    
    # 分析训练集
    all_train_signals = []
    for start_date, end_date in train_periods:
        logger.info(f"\n分析训练集: {start_date} ~ {end_date}")
        df = analyze_signals_for_period(
            jq,
            start_date,
            end_date,
            universe=None,
            max_stocks=300,  # 限制股票数量以加速
            rebalance_days=5,
            **signal_params
        )
        if not df.empty:
            all_train_signals.append(df)
    
    if not all_train_signals:
        logger.error("训练集未找到任何信号")
        return
    
    train_df = pd.concat(all_train_signals, ignore_index=True)
    logger.info(f"\n✅ 训练集共找到 {len(train_df)} 个信号")
    
    # 统计分析
    logger.info("\n" + "=" * 70)
    logger.info("信号统计分析")
    logger.info("=" * 70)
    
    stats = analyze_signal_statistics(train_df)
    
    # 打印统计结果
    print("\n📊 信号类型统计:")
    print("-" * 70)
    for signal_type, stat in stats.items():
        if signal_type == 'overall' or signal_type == 'correlation':
            continue
        print(f"\n{signal_type}:")
        print(f"  数量: {stat['count']}")
        print(f"  频率: {stat['frequency']:.2f}%")
        print(f"  平均收益: {stat['avg_return']:.2f}%")
        print(f"  中位数收益: {stat['median_return']:.2f}%")
        print(f"  胜率: {stat['win_rate']:.2f}%")
        print(f"  平均评分: {stat['avg_score']:.1f}")
    
    if 'overall' in stats:
        print(f"\n📈 总体统计:")
        print(f"  总信号数: {stats['overall']['total_signals']}")
        print(f"  平均收益: {stats['overall']['avg_return']:.2f}%")
        print(f"  胜率: {stats['overall']['win_rate']:.2f}%")
        print(f"  平均评分: {stats['overall']['avg_score']:.1f}")
    
    if 'correlation' in stats:
        print(f"\n📊 相关性分析:")
        print(f"  评分 vs 收益率: {stats['correlation']['score_vs_return']:.4f}")
    
    # 保存结果
    output_dir = PROJECT_ROOT / 'output' / 'chase_rise_analysis'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存DataFrame
    csv_path = output_dir / f'signals_{timestamp}.csv'
    train_df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    logger.info(f"\n✅ 信号数据已保存: {csv_path}")
    
    # 保存统计结果
    json_path = output_dir / f'statistics_{timestamp}.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2, default=str)
    logger.info(f"✅ 统计结果已保存: {json_path}")
    
    logger.info("\n" + "=" * 70)
    logger.info("分析完成")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
