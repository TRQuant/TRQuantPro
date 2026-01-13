#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
================================================================================
牛市高收益策略优化 - 滚动回测验证
================================================================================

使用2019年初到2021年初的历史牛市数据进行滚动回测，
优化选股算法，提升策略在牛市中的表现。

作者: TRQuant Team
日期: 2026-01-10
================================================================================
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import logging
import json

# 设置项目根路径
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 设置JQData环境变量
os.environ['JQDATA_USERNAME'] = '13327806797'
os.environ['JQDATA_PASSWORD'] = 'Taorui888'

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入JQData
import jqdatasdk as jq
jq.auth('13327806797', 'Taorui888')


def analyze_market_periods():
    """分析2019-2021牛市的不同阶段"""
    logger.info("=" * 60)
    logger.info("分析2019-2021牛市阶段")
    logger.info("=" * 60)
    
    # 获取沪深300指数数据
    index_data = jq.get_price(
        '000300.XSHG',
        start_date='2019-01-01',
        end_date='2021-03-31',
        frequency='daily',
        fields=['close', 'volume', 'money'],
        fq='post'
    )
    
    if index_data.empty:
        logger.error("获取指数数据失败")
        return None
    
    # 计算技术指标
    index_data['ma_20'] = index_data['close'].rolling(20).mean()
    index_data['ma_60'] = index_data['close'].rolling(60).mean()
    index_data['mom_20d'] = index_data['close'].pct_change(20) * 100
    index_data['mom_60d'] = index_data['close'].pct_change(60) * 100
    
    # 定义市场状态
    def detect_state(row):
        if pd.isna(row['mom_20d']) or pd.isna(row['mom_60d']):
            return 'NEUTRAL'
        if row['mom_20d'] > 10 and row['mom_60d'] > 20:
            return 'BULL'
        elif row['mom_20d'] < -10 and row['mom_60d'] < -10:
            return 'BEAR'
        else:
            return 'NEUTRAL'
    
    index_data['market_state'] = index_data.apply(detect_state, axis=1)
    
    # 统计市场状态分布
    state_counts = index_data['market_state'].value_counts()
    logger.info(f"市场状态分布:")
    for state, count in state_counts.items():
        pct = count / len(index_data) * 100
        logger.info(f"  {state}: {count}天 ({pct:.1f}%)")
    
    # 识别牛市阶段
    bull_periods = []
    in_bull = False
    start_date = None
    
    for date, row in index_data.iterrows():
        if row['market_state'] == 'BULL' and not in_bull:
            in_bull = True
            start_date = date
        elif row['market_state'] != 'BULL' and in_bull:
            in_bull = False
            bull_periods.append((start_date, date))
            start_date = None
    
    if in_bull and start_date:
        bull_periods.append((start_date, index_data.index[-1]))
    
    logger.info(f"\n识别到{len(bull_periods)}个牛市阶段:")
    for i, (start, end) in enumerate(bull_periods):
        days = (end - start).days
        logger.info(f"  阶段{i+1}: {start.strftime('%Y-%m-%d')} ~ {end.strftime('%Y-%m-%d')} ({days}天)")
    
    return index_data, bull_periods


def find_high_return_stocks(start_date: str, end_date: str, min_return: float = 30.0):
    """
    挖掘指定时间段内的高回报股票
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        min_return: 最小收益率 (%)
        
    Returns:
        高回报股票列表
    """
    logger.info(f"\n挖掘高回报股票: {start_date} ~ {end_date}")
    
    # 获取全A股股票（不限于指数成分股）
    all_stocks_df = jq.get_all_securities(types=['stock'], date=start_date)
    stocks = list(all_stocks_df.index)
    
    # 过滤ST和北交所
    filtered_stocks = []
    for stock in stocks:
        if 'ST' in all_stocks_df.loc[stock, 'display_name']:
            continue
        if stock.startswith('8') or stock.startswith('430'):
            continue
        filtered_stocks.append(stock)
    
    stocks = filtered_stocks
    logger.info(f"全A股股票池: {len(stocks)}只 (排除ST/北交所)")
    
    # 分批获取价格数据（JQData限制每次1000只股票）
    batch_size = 500
    all_prices = []
    
    for i in range(0, len(stocks), batch_size):
        batch_stocks = stocks[i:i+batch_size]
        logger.info(f"  获取价格数据: 批次{i//batch_size + 1}, 股票{len(batch_stocks)}只...")
        
        try:
            batch_prices = jq.get_price(
                batch_stocks,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['close', 'high', 'low', 'volume', 'money'],
                panel=False,
                fq='post'
            )
            if batch_prices is not None and not batch_prices.empty:
                all_prices.append(batch_prices)
        except Exception as e:
            logger.warning(f"  批次{i//batch_size + 1}获取失败: {e}")
            continue
    
    if not all_prices:
        logger.warning("获取价格数据失败")
        return []
    
    prices = pd.concat(all_prices, ignore_index=True)
    logger.info(f"价格数据总量: {len(prices)}条")
    
    high_return_stocks = []
    
    for stock in stocks:
        try:
            stock_data = prices[prices['code'] == stock].sort_values('time')
            
            if len(stock_data) < 20:
                continue
            
            # 计算周收益
            for i in range(0, len(stock_data) - 5, 5):
                start_price = stock_data.iloc[i]['close']
                end_price = stock_data.iloc[min(i+5, len(stock_data)-1)]['close']
                
                if start_price > 0:
                    weekly_return = (end_price / start_price - 1) * 100
                    
                    if weekly_return >= min_return:
                        trade_date = stock_data.iloc[i]['time']
                        
                        # 获取买入前的因子数据
                        prev_data = stock_data.iloc[max(0, i-20):i+1]
                        
                        if len(prev_data) >= 10:
                            close_arr = prev_data['close'].values
                            high_arr = prev_data['high'].values
                            low_arr = prev_data['low'].values
                            volume_arr = prev_data['volume'].values
                            
                            # 计算因子
                            mom_5d = (close_arr[-1] / close_arr[-6] - 1) * 100 if len(close_arr) >= 6 else 0
                            mom_20d = (close_arr[-1] / close_arr[0] - 1) * 100 if len(close_arr) >= 20 else 0
                            
                            high_20 = np.max(high_arr)
                            low_20 = np.min(low_arr)
                            rel_pos = (close_arr[-1] - low_20) / (high_20 - low_20) * 100 if high_20 > low_20 else 50
                            
                            vol_ratio = volume_arr[-1] / np.mean(volume_arr[:-1]) if len(volume_arr) > 1 and np.mean(volume_arr[:-1]) > 0 else 1
                            
                            # 检测涨停
                            is_limit_up = close_arr[-1] / close_arr[-2] - 1 > 0.095 if len(close_arr) >= 2 else False
                            
                            high_return_stocks.append({
                                'code': stock,
                                'date': trade_date,
                                'weekly_return': weekly_return,
                                'mom_5d': mom_5d,
                                'mom_20d': mom_20d,
                                'rel_position': rel_pos,
                                'volume_ratio': vol_ratio,
                                'is_limit_up': is_limit_up
                            })
                            
        except Exception as e:
            continue
    
    logger.info(f"找到 {len(high_return_stocks)} 个高回报案例 (周收益≥{min_return}%)")
    return high_return_stocks


def analyze_winning_factors(high_return_cases: list):
    """分析高回报案例的共同因子特征"""
    if not high_return_cases:
        logger.warning("无高回报案例")
        return None
    
    df = pd.DataFrame(high_return_cases)
    
    logger.info("\n" + "=" * 60)
    logger.info("高回报股票因子特征分析")
    logger.info("=" * 60)
    
    # 基本统计
    logger.info(f"\n案例数量: {len(df)}")
    logger.info(f"平均周收益: {df['weekly_return'].mean():.1f}%")
    logger.info(f"最高周收益: {df['weekly_return'].max():.1f}%")
    
    # 因子分布
    logger.info("\n因子分布 (均值 ± 标准差):")
    for col in ['mom_5d', 'mom_20d', 'rel_position', 'volume_ratio']:
        mean_val = df[col].mean()
        std_val = df[col].std()
        logger.info(f"  {col}: {mean_val:.2f} ± {std_val:.2f}")
    
    # 涨停占比
    limit_up_pct = df['is_limit_up'].sum() / len(df) * 100
    logger.info(f"\n涨停股占比: {limit_up_pct:.1f}%")
    
    # 分位数分析
    logger.info("\n因子分位数:")
    for col in ['mom_5d', 'mom_20d', 'rel_position', 'volume_ratio']:
        q25 = df[col].quantile(0.25)
        q50 = df[col].quantile(0.50)
        q75 = df[col].quantile(0.75)
        logger.info(f"  {col}: Q25={q25:.1f}, Q50={q50:.1f}, Q75={q75:.1f}")
    
    # 关键发现
    logger.info("\n" + "=" * 60)
    logger.info("关键发现 - 高回报股票特征:")
    logger.info("=" * 60)
    
    # 动量特征
    strong_mom_5d = df[df['mom_5d'] > 10]
    strong_mom_20d = df[df['mom_20d'] > 15]
    logger.info(f"  5日动量>10%的案例: {len(strong_mom_5d)} ({len(strong_mom_5d)/len(df)*100:.1f}%)")
    logger.info(f"  20日动量>15%的案例: {len(strong_mom_20d)} ({len(strong_mom_20d)/len(df)*100:.1f}%)")
    
    # 位置特征
    high_pos = df[df['rel_position'] > 70]
    mid_pos = df[(df['rel_position'] >= 40) & (df['rel_position'] <= 70)]
    low_pos = df[df['rel_position'] < 40]
    logger.info(f"  高位（>70%）: {len(high_pos)} ({len(high_pos)/len(df)*100:.1f}%)")
    logger.info(f"  中位（40-70%）: {len(mid_pos)} ({len(mid_pos)/len(df)*100:.1f}%)")
    logger.info(f"  低位（<40%）: {len(low_pos)} ({len(low_pos)/len(df)*100:.1f}%)")
    
    # 量比特征
    high_vol = df[df['volume_ratio'] > 2]
    logger.info(f"  量比>2的案例: {len(high_vol)} ({len(high_vol)/len(df)*100:.1f}%)")
    
    return df


def recommend_optimal_strategy(factor_analysis: pd.DataFrame):
    """基于因子分析推荐最优策略参数"""
    logger.info("\n" + "=" * 60)
    logger.info("推荐策略参数")
    logger.info("=" * 60)
    
    # 基于分位数设置阈值
    mom_5d_threshold = factor_analysis['mom_5d'].quantile(0.25)
    mom_20d_threshold = factor_analysis['mom_20d'].quantile(0.25)
    rel_pos_threshold = factor_analysis['rel_position'].quantile(0.25)
    vol_ratio_threshold = factor_analysis['volume_ratio'].quantile(0.25)
    
    logger.info("\n1. 追涨策略（牛市模式）:")
    logger.info(f"   - 5日动量 >= {max(5, mom_5d_threshold):.0f}%")
    logger.info(f"   - 20日动量 >= {max(10, mom_20d_threshold):.0f}%")
    logger.info(f"   - 相对位置 >= {max(50, rel_pos_threshold):.0f}%")
    logger.info(f"   - 量比 >= {max(1.5, vol_ratio_threshold):.1f}")
    
    # 涨停策略
    limit_up_cases = factor_analysis[factor_analysis['is_limit_up'] == True]
    if len(limit_up_cases) > 0:
        avg_return = limit_up_cases['weekly_return'].mean()
        logger.info(f"\n2. 涨停板追涨策略:")
        logger.info(f"   - 涨停案例数: {len(limit_up_cases)}")
        logger.info(f"   - 平均后续周收益: {avg_return:.1f}%")
        logger.info(f"   - 配合放量（量比>2）效果更佳")
    
    # 生成优化后的策略参数
    optimal_params = {
        'SIGNAL_THRESHOLD': 50,  # 降低信号阈值
        'MIN_MOMENTUM_5D': max(5, mom_5d_threshold),
        'MIN_MOMENTUM_20D': max(10, mom_20d_threshold),
        'MIN_REL_POSITION': max(50, rel_pos_threshold),  # 追涨应该是高位
        'MIN_VOLUME_RATIO': max(1.5, vol_ratio_threshold),
        'VOLUME_EXPLOSION_THRESHOLD': 2.5,
        'STOP_LOSS_PCT': -8,
        'TAKE_PROFIT_PCT': 25,
        'MAX_POSITIONS': 2,
        'REBALANCE_DAYS': 5
    }
    
    logger.info("\n3. 优化后的策略参数:")
    for key, value in optimal_params.items():
        logger.info(f"   {key} = {value}")
    
    return optimal_params


def run_rolling_backtest(start_date: str, end_date: str, params: dict):
    """
    使用BulletTrade运行滚动回测
    """
    logger.info("\n" + "=" * 60)
    logger.info(f"滚动回测: {start_date} ~ {end_date}")
    logger.info("=" * 60)
    
    # 导入BulletTrade引擎
    try:
        from core.bullettrade.engine import BulletTradeEngine
        from core.bullettrade.config import BTConfig
    except ImportError as e:
        logger.error(f"导入BulletTrade失败: {e}")
        return None
    
    # 生成优化后的策略代码
    strategy_code = generate_optimized_strategy_code(params)
    
    # 配置回测
    config = BTConfig(
        start_date=start_date,
        end_date=end_date,
        initial_capital=1000000,
        benchmark='000300.XSHG',
        output_dir=str(PROJECT_ROOT / 'output' / 'optimization_backtest')
    )
    
    # 运行回测
    engine = BulletTradeEngine(config)
    result = engine.run_backtest(strategy_code=strategy_code)
    
    if result:
        logger.info(f"\n回测结果:")
        logger.info(f"  总收益率: {result.total_return:.2f}%")
        logger.info(f"  年化收益: {result.annual_return:.2f}%")
        logger.info(f"  最大回撤: {result.max_drawdown:.2f}%")
        logger.info(f"  夏普比率: {result.sharpe_ratio:.2f}")
        logger.info(f"  交易次数: {result.total_trades}")
        logger.info(f"  胜率: {result.trade_win_rate:.2f}%")
    
    return result


def generate_optimized_strategy_code(params: dict) -> str:
    """生成优化后的策略代码"""
    code = f'''# -*- coding: utf-8 -*-
"""
================================================================================
优化后的牛市高收益策略 - 基于2019-2021历史数据
================================================================================
"""

import numpy as np
import pandas as pd
import jqdatasdk
from jqdatasdk import query, valuation, get_fundamentals

# JQData认证
try:
    jqdatasdk.auth('13327806797', 'Taorui888')
except:
    pass

# ======================= 优化后的策略参数 =======================
SIGNAL_THRESHOLD = {params.get('SIGNAL_THRESHOLD', 50)}
MIN_MOMENTUM_5D = {params.get('MIN_MOMENTUM_5D', 5)}
MIN_MOMENTUM_20D = {params.get('MIN_MOMENTUM_20D', 10)}
MIN_REL_POSITION = {params.get('MIN_REL_POSITION', 50)}  # 追涨策略需要股票在相对高位
MIN_VOLUME_RATIO = {params.get('MIN_VOLUME_RATIO', 1.5)}
VOLUME_EXPLOSION_THRESHOLD = {params.get('VOLUME_EXPLOSION_THRESHOLD', 2.5)}
STOP_LOSS_PCT = {params.get('STOP_LOSS_PCT', -8)}
TAKE_PROFIT_PCT = {params.get('TAKE_PROFIT_PCT', 25)}
MAX_POSITIONS = {params.get('MAX_POSITIONS', 2)}
REBALANCE_DAYS = {params.get('REBALANCE_DAYS', 5)}
POSITION_SIZE_PCT = 50


def initialize(context):
    """初始化"""
    set_benchmark('000300.XSHG')
    set_option('use_real_price', True)
    
    set_order_cost(OrderCost(
        open_tax=0,
        close_tax=0.001,
        open_commission=0.0003,
        close_commission=0.0003,
        min_commission=5
    ), type='stock')
    
    context.rebalance_day = 0
    context.cost_prices = {{}}
    
    run_daily(before_trading_start, time='09:00')
    run_daily(handle_data, time='09:35')
    run_daily(check_risk_control, time='14:50')
    
    log.info("=" * 60)
    log.info("优化后的牛市高收益策略初始化完成")
    log.info(f"追涨参数: 5日动量>={{MIN_MOMENTUM_5D}}%, 20日动量>={{MIN_MOMENTUM_20D}}%")
    log.info(f"相对位置>={{MIN_REL_POSITION}}%, 量比>={{MIN_VOLUME_RATIO}}")
    log.info("=" * 60)


def before_trading_start(context):
    """盘前处理"""
    current_date = context.current_dt.strftime('%Y-%m-%d')
    try:
        # 获取全A股（不限于指数成分股）
        all_stocks_df = get_all_securities(types=['stock'], date=current_date)
        all_stocks = list(all_stocks_df.index)
        
        # 过滤ST和北交所
        filtered_stocks = []
        for stock in all_stocks:
            if 'ST' in all_stocks_df.loc[stock, 'display_name']:
                continue
            if stock.startswith('8') or stock.startswith('430'):
                continue
            filtered_stocks.append(stock)
        
        context.universe = filtered_stocks
        log.info(f"[盘前] 全A股股票池: {{len(context.universe)}}只")
    except Exception as e:
        log.error(f"[盘前] 获取股票池失败: {{e}}")
        context.universe = []


def handle_data(context):
    """每日交易处理"""
    context.rebalance_day += 1
    
    if context.rebalance_day % REBALANCE_DAYS != 0:
        return
    
    log.info(f"[调仓日] 第{{context.rebalance_day}}天")
    
    signals = generate_momentum_signals(context)
    
    if not signals:
        log.info("[调仓] 无有效信号")
        return
    
    log.info(f"[调仓] 有效信号: {{len(signals)}}个")
    
    # 显示TOP信号
    for s in signals[:5]:
        log.info(f"  {{s['code']}}: 评分={{s['score']:.0f}}, 5日动量={{s.get('mom_5d', 0):.1f}}%, 量比={{s.get('vol_ratio', 1):.1f}}")
    
    execute_trades(context, signals)


def generate_momentum_signals(context):
    """
    生成动量追涨信号
    
    核心逻辑：
    1. 筛选强势动量股（5日动量>阈值，20日动量>阈值）
    2. 要求股票在相对高位（不是低位抄底）
    3. 放量确认
    """
    signals = []
    current_date = context.current_dt.strftime('%Y-%m-%d')
    
    for stock in context.universe:
        try:
            # 获取价格数据
            prices = get_price(
                stock,
                end_date=current_date,
                count=25,
                frequency='daily',
                fields=['close', 'high', 'low', 'volume', 'money'],
                fq='post'
            )
            
            if len(prices) < 21:
                continue
            
            close = prices['close'].values
            high = prices['high'].values
            low = prices['low'].values
            volume = prices['volume'].values
            
            # ====== 计算因子 ======
            
            # 动量
            mom_5d = (close[-1] / close[-6] - 1) * 100 if len(close) >= 6 else 0
            mom_20d = (close[-1] / close[-21] - 1) * 100 if len(close) >= 21 else 0
            
            # 相对位置
            high_20 = np.max(high[-20:])
            low_20 = np.min(low[-20:])
            rel_pos = (close[-1] - low_20) / (high_20 - low_20) * 100 if high_20 > low_20 else 50
            
            # 量比
            vol_ratio = volume[-1] / np.mean(volume[-20:-1]) if np.mean(volume[-20:-1]) > 0 else 1
            
            # 涨停检测
            is_limit_up = close[-1] / close[-2] - 1 > 0.095 if len(close) >= 2 else False
            
            # ====== 追涨信号评分 ======
            score = 0
            signal_type = 'NO_SIGNAL'
            
            # 信号1: 涨停板+放量 (最强信号)
            if is_limit_up and vol_ratio > VOLUME_EXPLOSION_THRESHOLD:
                score = 80
                signal_type = 'LIMIT_UP_VOLUME'
            
            # 信号2: 涨停板
            elif is_limit_up:
                score = 65
                signal_type = 'LIMIT_UP'
            
            # 信号3: 强动量+高位+放量
            elif (mom_5d >= MIN_MOMENTUM_5D and 
                  mom_20d >= MIN_MOMENTUM_20D and 
                  rel_pos >= MIN_REL_POSITION and
                  vol_ratio >= MIN_VOLUME_RATIO):
                score = 60
                
                # 加分项
                if mom_5d > 15:
                    score += 10
                if vol_ratio > 2:
                    score += 10
                if rel_pos > 80:
                    score += 5
                
                signal_type = 'STRONG_MOMENTUM'
            
            # 信号4: 突破新高+放量
            elif (close[-1] > np.max(high[-60:-1]) if len(high) >= 60 else False) and vol_ratio > 1.5:
                score = 55
                signal_type = 'BREAKOUT'
            
            # 筛选有效信号
            if score >= SIGNAL_THRESHOLD and signal_type != 'NO_SIGNAL':
                signals.append({{
                    'code': stock,
                    'score': score,
                    'signal_type': signal_type,
                    'mom_5d': mom_5d,
                    'mom_20d': mom_20d,
                    'rel_pos': rel_pos,
                    'vol_ratio': vol_ratio,
                    'is_limit_up': is_limit_up
                }})
                
        except Exception as e:
            continue
    
    # 按评分排序
    signals.sort(key=lambda x: x['score'], reverse=True)
    
    return signals


def execute_trades(context, signals):
    """执行交易"""
    target_stocks = [s['code'] for s in signals[:MAX_POSITIONS]]
    
    log.info(f"[交易] 目标股票: {{target_stocks}}")
    
    # 卖出不在目标列表的股票
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.total_amount == 0:
            continue
        
        if stock not in target_stocks:
            order_target(stock, 0)
            log.info(f"[卖出-轮动] {{stock}}")
            context.cost_prices.pop(stock, None)
    
    if not target_stocks:
        return
    
    # 买入目标股票
    total_value = context.portfolio.total_value
    per_stock_value = total_value * POSITION_SIZE_PCT / 100
    
    for stock in target_stocks:
        if stock in context.portfolio.positions:
            pos = context.portfolio.positions[stock]
            if pos.total_amount > 0:
                continue
        
        current_data = get_current_data()
        if stock in current_data:
            stock_data = current_data[stock]
            if hasattr(stock_data, 'paused') and stock_data.paused:
                continue
            if hasattr(stock_data, 'is_limit_up') and stock_data.is_limit_up:
                continue
        
        order_value(stock, per_stock_value)
        
        # 获取成本价
        try:
            current_price = get_current_data()[stock].last_price
            context.cost_prices[stock] = current_price
        except:
            pass
        
        # 查找信号信息
        signal_info = next((s for s in signals if s['code'] == stock), {{}})
        log.info(f"[买入] {{stock}}: 评分={{signal_info.get('score', 0):.0f}}, 类型={{signal_info.get('signal_type', 'N/A')}}")


def check_risk_control(context):
    """风控检查"""
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        if pos.total_amount == 0:
            continue
        
        cost_price = context.cost_prices.get(stock, pos.avg_cost)
        if cost_price <= 0:
            cost_price = pos.avg_cost
        
        current_price = pos.price
        pnl_pct = (current_price / cost_price - 1) * 100
        
        # 止损
        if pnl_pct <= STOP_LOSS_PCT:
            order_target(stock, 0)
            log.info(f"[止损] {{stock}}: 亏损{{pnl_pct:.1f}}%")
            context.cost_prices.pop(stock, None)
        
        # 止盈
        elif pnl_pct >= TAKE_PROFIT_PCT:
            order_target(stock, 0)
            log.info(f"[止盈] {{stock}}: 盈利{{pnl_pct:.1f}}%")
            context.cost_prices.pop(stock, None)
'''
    return code


def main():
    """主函数"""
    logger.info("=" * 70)
    logger.info("牛市高收益策略优化 - 基于2019-2021历史数据")
    logger.info("=" * 70)
    
    # 1. 分析市场阶段
    market_analysis = analyze_market_periods()
    
    # 2. 挖掘高回报股票
    high_return_cases = find_high_return_stocks(
        start_date='2019-01-01',
        end_date='2021-03-31',
        min_return=20.0  # 周收益>20%
    )
    
    # 3. 分析高回报因子特征
    factor_analysis = None
    if high_return_cases:
        factor_analysis = analyze_winning_factors(high_return_cases)
    
    # 4. 推荐最优策略参数
    optimal_params = None
    if factor_analysis is not None:
        optimal_params = recommend_optimal_strategy(factor_analysis)
    else:
        # 默认参数
        optimal_params = {
            'SIGNAL_THRESHOLD': 50,
            'MIN_MOMENTUM_5D': 8,
            'MIN_MOMENTUM_20D': 12,
            'MIN_REL_POSITION': 55,
            'MIN_VOLUME_RATIO': 1.5,
            'VOLUME_EXPLOSION_THRESHOLD': 2.5,
            'STOP_LOSS_PCT': -8,
            'TAKE_PROFIT_PCT': 25,
            'MAX_POSITIONS': 2,
            'REBALANCE_DAYS': 5
        }
    
    # 5. 滚动回测验证
    logger.info("\n" + "=" * 60)
    logger.info("开始滚动回测验证")
    logger.info("=" * 60)
    
    # 测试不同时间段
    test_periods = [
        ('2019-01-01', '2019-06-30', '2019上半年'),
        ('2019-07-01', '2019-12-31', '2019下半年'),
        ('2020-01-01', '2020-06-30', '2020上半年'),
        ('2020-07-01', '2020-12-31', '2020下半年'),
    ]
    
    results = []
    for start, end, period_name in test_periods:
        logger.info(f"\n--- 回测期: {period_name} ({start} ~ {end}) ---")
        result = run_rolling_backtest(start, end, optimal_params)
        if result:
            results.append({
                'period': period_name,
                'start': start,
                'end': end,
                'total_return': result.total_return,
                'annual_return': result.annual_return,
                'max_drawdown': result.max_drawdown,
                'sharpe_ratio': result.sharpe_ratio,
                'trades': result.total_trades,
                'win_rate': result.trade_win_rate
            })
    
    # 6. 汇总结果
    if results:
        logger.info("\n" + "=" * 70)
        logger.info("滚动回测汇总")
        logger.info("=" * 70)
        
        df_results = pd.DataFrame(results)
        logger.info(f"\n{df_results.to_string()}")
        
        # 计算平均表现
        avg_return = df_results['total_return'].mean()
        avg_sharpe = df_results['sharpe_ratio'].mean()
        avg_win_rate = df_results['win_rate'].mean()
        
        logger.info(f"\n平均表现:")
        logger.info(f"  平均总收益: {avg_return:.2f}%")
        logger.info(f"  平均夏普比率: {avg_sharpe:.2f}")
        logger.info(f"  平均胜率: {avg_win_rate:.2f}%")
        
        # 保存结果
        output_path = PROJECT_ROOT / 'output' / 'optimization_results.json'
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                'optimal_params': optimal_params,
                'backtest_results': results,
                'summary': {
                    'avg_return': avg_return,
                    'avg_sharpe': avg_sharpe,
                    'avg_win_rate': avg_win_rate
                }
            }, f, ensure_ascii=False, indent=2)
        
        logger.info(f"\n结果已保存: {output_path}")
    
    logger.info("\n" + "=" * 70)
    logger.info("优化完成")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
