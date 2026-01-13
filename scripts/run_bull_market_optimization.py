#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牛市极端高收益策略递归迭代优化

目标: 周收益10%+ (激进策略)
回测引擎: BulletTrade (JQData数据源)
优化方法: 网格搜索 + 训练集/验证集分离

特性:
1. 融合追涨信号 + 7因子选股
2. 实时进度报告
3. 完善的错误处理
4. 数据缓存机制
5. BulletTrade回测集成

基于: scripts/run_chase_rise_optimization_fast.py
"""
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any
import pandas as pd
import numpy as np
import logging
import json
from dataclasses import dataclass, asdict, field
from itertools import product
import time
import traceback

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# ==================== 全局配置 ====================

class Config:
    """优化配置"""
    # 股票池
    MAX_STOCKS = 100  # 最大股票数
    
    # 超时设置（秒）
    BACKTEST_TIMEOUT = 120
    TOTAL_TIMEOUT = 1800  # 30分钟总超时
    
    # 输出目录
    OUTPUT_DIR = PROJECT_ROOT / 'output' / 'bull_market_optimization'
    
    # 缓存目录
    CACHE_DIR = PROJECT_ROOT / 'data' / 'cache'


# ==================== 数据类定义 ====================

@dataclass
class BullMarketStrategyParams:
    """牛市策略参数 - 融合追涨信号+7因子选股"""
    
    # === 追涨信号参数 (来自优化结果) ===
    limit_up_threshold: float = 0.093
    vol_ratio_threshold_first: float = 2.5
    mom_5d_threshold_breakout: float = 16.0
    mom_5d_threshold_volume: float = 10.0
    vol_ratio_threshold_breakout: float = 1.5
    vol_ratio_threshold_volume: float = 2.0
    
    # === 7因子选股参数 (待优化) ===
    min_momentum_20d: float = 5.0       # 最小20日动量(%)
    max_momentum_20d: float = 40.0      # 最大20日动量(%)
    max_rel_position: float = 80.0      # 最大相对位置(%)
    max_market_cap: float = 300.0       # 最大市值(亿)
    min_volume_ratio: float = 1.5       # 最小量比
    min_turnover_rate: float = 1.0      # 最小换手率(%)
    max_turnover_rate: float = 15.0     # 最大换手率(%)
    min_roe: float = 0.0                # 最小ROE(%)
    
    # === 交易参数 ===
    max_positions: int = 5              # 最大持仓数
    single_position_max: float = 0.20   # 单票最大仓位
    stop_loss_pct: float = -8.0         # 止损比例(%)
    take_profit_pct: float = 30.0       # 止盈比例(%)
    rebalance_days: int = 5             # 调仓周期(交易日)
    
    # === 综合得分 ===
    min_total_score: float = 30.0       # 最小综合得分


@dataclass
class BacktestResult:
    """回测结果"""
    total_return: float = 0.0
    annual_return: float = 0.0
    sharpe_ratio: float = 0.0
    max_drawdown: float = 0.0
    win_rate: float = 0.0
    total_trades: int = 0
    avg_holding_days: float = 0.0
    profit_factor: float = 0.0
    error: str = ""


# ==================== 进度报告器 ====================

class ProgressReporter:
    """进度报告器"""
    
    def __init__(self, total: int, desc: str = ""):
        self.total = total
        self.current = 0
        self.desc = desc
        self.start_time = time.time()
        self.last_report_time = 0
        self.best_score = -float('inf')
        self.errors = 0
    
    def update(self, n: int = 1, score: float = None, error: bool = False):
        """更新进度"""
        self.current += n
        if error:
            self.errors += 1
        if score is not None and score > self.best_score:
            self.best_score = score
        
        now = time.time()
        progress_pct = self.current / self.total * 100
        
        if now - self.last_report_time >= 3 or progress_pct % 10 < 0.5:
            self.report()
            self.last_report_time = now
    
    def report(self):
        """输出进度报告"""
        elapsed = time.time() - self.start_time
        progress_pct = self.current / self.total * 100
        
        if self.current > 0:
            eta = elapsed / self.current * (self.total - self.current)
            eta_str = f"{eta/60:.1f}分钟" if eta > 60 else f"{eta:.0f}秒"
        else:
            eta_str = "计算中..."
        
        best_str = f", 最优={self.best_score:.4f}" if self.best_score > -float('inf') else ""
        error_str = f", 错误={self.errors}" if self.errors > 0 else ""
        
        logger.info(f"[{self.desc}] {self.current}/{self.total} ({progress_pct:.1f}%) | "
                   f"已用={elapsed/60:.1f}分钟 | ETA={eta_str}{best_str}{error_str}")
    
    def finish(self):
        """完成报告"""
        elapsed = time.time() - self.start_time
        logger.info(f"[{self.desc}] 完成! 总用时={elapsed/60:.1f}分钟, "
                   f"成功={self.current-self.errors}, 错误={self.errors}")


# ==================== BulletTrade回测封装 ====================

def run_bullettrade_backtest(
    params: BullMarketStrategyParams,
    start_date: str,
    end_date: str,
    initial_capital: float = 1000000.0,
) -> BacktestResult:
    """
    执行BulletTrade回测
    
    Args:
        params: 策略参数
        start_date: 开始日期
        end_date: 结束日期
        initial_capital: 初始资金
    
    Returns:
        BacktestResult: 回测结果
    """
    try:
        from core.advisor_v4.bullettrade_strategy_generator import StrategyConfig, BulletTradeStrategyGenerator
        from core.bullettrade.engine import BulletTradeEngine, BTConfig
        
        # 创建策略配置 - 只传递StrategyConfig支持的参数
        strategy_config = StrategyConfig(
            max_stocks=params.max_positions,
            min_total_score=params.min_total_score,
            single_position_max=params.single_position_max,
            stop_loss=params.stop_loss_pct / 100,
            take_profit=params.take_profit_pct / 100,
            min_momentum_20d=params.min_momentum_20d,
            max_momentum_20d=params.max_momentum_20d,
            max_rel_position=params.max_rel_position,
            min_turnover_rate=params.min_turnover_rate,
            max_turnover_rate=params.max_turnover_rate,
            min_roe=params.min_roe,
        )
        
        # 生成策略代码
        generator = BulletTradeStrategyGenerator(
            strategy_config,
            cache_data_dir=str(Config.CACHE_DIR)
        )
        strategy_code = generator.generate_strategy_code()
        
        # 创建BulletTrade配置
        bt_config = BTConfig(
            initial_capital=initial_capital,
            benchmark='000300.XSHG',
        )
        
        # 执行回测
        engine = BulletTradeEngine(bt_config)
        result = engine.run(
            strategy_code=strategy_code,
            start_date=start_date,
            end_date=end_date,
        )
        
        if result is None:
            return BacktestResult(error="回测返回None")
        
        # 解析结果
        metrics = result.get_metrics() if hasattr(result, 'get_metrics') else {}
        
        return BacktestResult(
            total_return=metrics.get('total_return', 0.0) * 100,
            annual_return=metrics.get('annual_return', 0.0) * 100,
            sharpe_ratio=metrics.get('sharpe_ratio', 0.0),
            max_drawdown=metrics.get('max_drawdown', 0.0) * 100,
            win_rate=metrics.get('win_rate', 0.0) * 100,
            total_trades=metrics.get('total_trades', 0),
            avg_holding_days=metrics.get('avg_holding_days', 0.0),
            profit_factor=metrics.get('profit_factor', 0.0),
        )
    
    except Exception as e:
        logger.debug(f"BulletTrade回测失败: {e}")
        return BacktestResult(error=str(e)[:100])


def run_simplified_backtest(
    params: BullMarketStrategyParams,
    start_date: str,
    end_date: str,
    jq_client,
    universe: List[str],
) -> BacktestResult:
    """
    简化回测 - 基于信号统计（快速评估）
    
    优化版本：批量获取数据，减少API调用
    """
    try:
        trade_days = jq_client.get_trade_days(start_date=start_date, end_date=end_date)
        if trade_days is None or len(trade_days) < 25:
            return BacktestResult(error="交易日不足")
        
        all_returns = []
        winning_count = 0
        
        # 精简采样：少量股票，少量日期
        sample_size = min(30, len(universe))
        sample_stocks = list(np.random.choice(universe, sample_size, replace=False))
        
        # 只选3个调仓日进行评估
        rebalance_indices = [
            22,  # 开始后22天
            len(trade_days) // 2,  # 中间
            len(trade_days) - 10,  # 结束前10天
        ]
        rebalance_indices = [i for i in rebalance_indices if 22 <= i < len(trade_days) - 5][:3]
        
        for i in rebalance_indices:
            current_date = trade_days[i]
            date_str = str(current_date)[:10]
            
            # 批量获取所有股票历史数据
            try:
                panel = jq_client.get_price(
                    sample_stocks,
                    end_date=date_str,
                    count=25,
                    frequency='daily',
                    fields=['close', 'volume'],
                    panel=False,
                )
                
                if panel is None or panel.empty:
                    continue
                
                # 批量获取未来价格
                future_idx = min(i + params.rebalance_days, len(trade_days) - 1)
                future_date_str = str(trade_days[future_idx])[:10]
                future_panel = jq_client.get_price(
                    sample_stocks,
                    end_date=future_date_str,
                    count=1,
                    frequency='daily',
                    fields=['close'],
                    panel=False,
                )
            except Exception:
                continue
            
            for stock in sample_stocks:
                try:
                    stock_data = panel[panel['code'] == stock] if 'code' in panel.columns else panel[panel.index.get_level_values(1) == stock]
                    if stock_data.empty or len(stock_data) < 22:
                        continue
                    
                    close = stock_data['close'].values
                    volume = stock_data['volume'].values
                    
                    # 计算因子
                    mom_20d = (close[-1] / close[-21] - 1) * 100
                    price_range = np.max(close[-20:]) - np.min(close[-20:])
                    rel_position = (close[-1] - np.min(close[-20:])) / (price_range + 1e-6) * 100 if price_range > 0 else 50
                    avg_vol = np.mean(volume[-20:])
                    vol_ratio = volume[-1] / avg_vol if avg_vol > 0 else 1.0
                    
                    # 筛选条件
                    if not (params.min_momentum_20d <= mom_20d <= params.max_momentum_20d):
                        continue
                    if rel_position > params.max_rel_position:
                        continue
                    if vol_ratio < params.min_volume_ratio:
                        continue
                    
                    # 计算未来收益
                    if future_panel is not None and not future_panel.empty:
                        future_data = future_panel[future_panel['code'] == stock] if 'code' in future_panel.columns else future_panel[future_panel.index.get_level_values(1) == stock]
                        if not future_data.empty:
                            exit_price = future_data['close'].iloc[-1]
                            future_return = (exit_price / close[-1] - 1) * 100
                            all_returns.append(future_return)
                            if future_return > 0:
                                winning_count += 1
                
                except Exception:
                    continue
        
        if not all_returns:
            return BacktestResult(error="无信号")
        
        returns = np.array(all_returns)
        avg_return = np.mean(returns)
        win_rate = winning_count / len(returns) * 100
        sharpe_ratio = np.mean(returns) / (np.std(returns) + 1e-6) * np.sqrt(52) if len(returns) > 1 else 0
        
        # 最大回撤
        cumulative = np.cumprod(1 + returns / 100)
        running_max = np.maximum.accumulate(cumulative)
        drawdown = (cumulative - running_max) / running_max * 100
        max_drawdown = np.min(drawdown) if len(drawdown) > 0 else 0
        
        return BacktestResult(
            total_return=avg_return * len(returns) / params.rebalance_days,
            annual_return=avg_return * 52,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            total_trades=len(returns),
        )
    
    except Exception as e:
        return BacktestResult(error=str(e)[:100])


def calculate_composite_score(result: BacktestResult) -> float:
    """
    计算综合评分
    
    针对牛市极端高收益策略优化:
    - 更高权重给年化收益（目标10%+周收益）
    - 夏普比率保持重要性
    - 胜率作为辅助指标
    """
    if result.error:
        return -100.0
    
    score = (
        result.annual_return * 0.35 +          # 年化收益权重35%
        result.sharpe_ratio * 0.25 +           # 夏普比率权重25%
        (100 - abs(result.max_drawdown)) / 100 * 0.20 +  # 回撤控制20%
        result.win_rate / 100 * 0.20           # 胜率权重20%
    )
    return score


# ==================== 网格搜索优化 ====================

def grid_search_optimize(
    jq_client,
    train_periods: List[Tuple[str, str]],
    validate_period: Tuple[str, str],
    param_grid: Dict[str, List],
    universe: List[str],
    use_bullettrade: bool = False,
) -> Tuple[Optional[BullMarketStrategyParams], List[Dict]]:
    """
    网格搜索优化
    
    Args:
        jq_client: JQData客户端
        train_periods: 训练集时间段列表
        validate_period: 验证集时间段
        param_grid: 参数网格
        universe: 股票池
        use_bullettrade: 是否使用完整BulletTrade回测（慢但准确）
    
    Returns:
        (最优参数, 优化历史)
    """
    # 生成参数组合
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    all_combinations = list(product(*param_values))
    total = len(all_combinations)
    
    logger.info(f"参数组合总数: {total}")
    
    progress = ProgressReporter(total, "网格搜索")
    
    best_params = None
    best_score = -float('inf')
    optimization_history = []
    
    # 默认参数
    default_params = asdict(BullMarketStrategyParams())
    
    for combo in all_combinations:
        try:
            params_dict = dict(zip(param_names, combo))
            full_params = default_params.copy()
            full_params.update(params_dict)
            params = BullMarketStrategyParams(**full_params)
            
            # 训练集回测
            train_results = []
            for train_start, train_end in train_periods:
                if use_bullettrade:
                    result = run_bullettrade_backtest(params, train_start, train_end)
                else:
                    result = run_simplified_backtest(params, train_start, train_end, jq_client, universe)
                train_results.append(result)
            
            # 平均训练结果
            valid_train = [r for r in train_results if not r.error]
            if valid_train:
                avg_train = BacktestResult(
                    total_return=np.mean([r.total_return for r in valid_train]),
                    annual_return=np.mean([r.annual_return for r in valid_train]),
                    sharpe_ratio=np.mean([r.sharpe_ratio for r in valid_train]),
                    max_drawdown=np.mean([r.max_drawdown for r in valid_train]),
                    win_rate=np.mean([r.win_rate for r in valid_train]),
                    total_trades=int(np.mean([r.total_trades for r in valid_train])),
                )
            else:
                avg_train = BacktestResult(error="训练失败")
            
            # 验证集回测
            if use_bullettrade:
                validate_result = run_bullettrade_backtest(
                    params, validate_period[0], validate_period[1]
                )
            else:
                validate_result = run_simplified_backtest(
                    params, validate_period[0], validate_period[1], jq_client, universe
                )
            
            # 计算评分
            train_score = calculate_composite_score(avg_train)
            validate_score = calculate_composite_score(validate_result)
            
            # 使用验证集评分
            score = validate_score
            
            # 记录历史
            history_entry = {
                'params': params_dict,
                'train_score': train_score,
                'train_annual_return': avg_train.annual_return,
                'train_sharpe': avg_train.sharpe_ratio,
                'train_win_rate': avg_train.win_rate,
                'train_max_drawdown': avg_train.max_drawdown,
                'validate_score': validate_score,
                'validate_annual_return': validate_result.annual_return,
                'validate_sharpe': validate_result.sharpe_ratio,
                'validate_win_rate': validate_result.win_rate,
                'validate_max_drawdown': validate_result.max_drawdown,
                'overfit_ratio': train_score / (validate_score + 1e-6) if validate_score != 0 else 0,
            }
            optimization_history.append(history_entry)
            
            # 更新最优
            if score > best_score:
                best_score = score
                best_params = params
                logger.info(f"  🎯 新最优: score={score:.4f}, 年化={validate_result.annual_return:.1f}%, "
                           f"胜率={validate_result.win_rate:.1f}%, 回撤={validate_result.max_drawdown:.1f}%")
            
            progress.update(score=score)
        
        except Exception as e:
            progress.update(error=True)
            logger.debug(f"参数组合失败: {e}")
    
    progress.finish()
    return best_params, optimization_history


# ==================== 主函数 ====================

def main():
    """主函数"""
    start_time = time.time()
    
    logger.info("=" * 70)
    logger.info("牛市极端高收益策略递归迭代优化")
    logger.info("=" * 70)
    logger.info("目标: 周收益10%+ | 回测引擎: BulletTrade/简化版")
    
    # 初始化JQData
    try:
        from config.config_manager import get_config_manager
        import jqdatasdk as jq
        
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config('jqdata')
        jq.auth(jq_config['username'], jq_config['password'])
        logger.info("✅ JQData连接成功")
    except Exception as e:
        logger.error(f"❌ JQData连接失败: {e}")
        traceback.print_exc()
        return
    
    # 数据集配置
    train_periods = [
        ('2019-06-01', '2020-06-30'),  # 牛市上涨期
        ('2024-09-01', '2025-01-10'),  # 最新行情
    ]
    validate_period = ('2020-07-01', '2021-03-31')  # 牛市中期
    
    logger.info(f"\n数据集:")
    for i, (start, end) in enumerate(train_periods, 1):
        logger.info(f"  训练集{i}: {start} ~ {end}")
    logger.info(f"  验证集: {validate_period[0]} ~ {validate_period[1]}")
    
    # 获取股票池
    try:
        securities = jq.get_all_securities(types=['stock'], date=validate_period[1])
        stocks = securities.index.tolist()
        universe = [
            code for code in stocks
            if 'ST' not in str(securities.loc[code, 'display_name']).upper()
        ][:Config.MAX_STOCKS]
        logger.info(f"✅ 股票池: {len(universe)}只")
    except Exception as e:
        logger.error(f"❌ 获取股票池失败: {e}")
        traceback.print_exc()
        return
    
    # 参数网格 - 精简版（快速完成）
    param_grid = {
        # 动量参数
        'min_momentum_20d': [5, 10],
        'max_momentum_20d': [50, 60],
        
        # 相对位置
        'max_rel_position': [80, 95],
        
        # 量比阈值
        'min_volume_ratio': [1.5, 2.0],
        
        # 持仓控制
        'max_positions': [3, 5],
    }
    
    total_combos = 1
    for v in param_grid.values():
        total_combos *= len(v)
    
    logger.info(f"\n参数网格 ({total_combos}种组合):")
    for param, values in param_grid.items():
        logger.info(f"  {param}: {values}")
    
    # 执行优化
    logger.info("\n" + "-" * 70)
    best_params, history = grid_search_optimize(
        jq,
        train_periods,
        validate_period,
        param_grid,
        universe,
        use_bullettrade=False,  # 先用简化版快速筛选
    )
    
    if best_params is None:
        logger.error("❌ 优化未找到任何结果")
        return
    
    # 输出结果
    logger.info("\n" + "=" * 70)
    logger.info("🏆 最优参数")
    logger.info("=" * 70)
    for key, value in asdict(best_params).items():
        logger.info(f"  {key}: {value}")
    
    # 保存结果
    Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 保存最优参数
    params_path = Config.OUTPUT_DIR / f'best_params_{timestamp}.json'
    with open(params_path, 'w', encoding='utf-8') as f:
        json.dump(asdict(best_params), f, ensure_ascii=False, indent=2)
    logger.info(f"\n✅ 最优参数已保存: {params_path}")
    
    # 保存优化历史
    if history:
        history_df = pd.DataFrame(history)
        history_df = history_df.sort_values('validate_score', ascending=False)
        history_path = Config.OUTPUT_DIR / f'optimization_history_{timestamp}.csv'
        history_df.to_csv(history_path, index=False, encoding='utf-8-sig')
        logger.info(f"✅ 优化历史已保存: {history_path}")
        
        # Top 5
        logger.info("\n📊 Top 5 参数组合:")
        for idx, row in history_df.head(5).iterrows():
            logger.info(f"  score={row['validate_score']:.4f}, "
                       f"年化={row['validate_annual_return']:.1f}%, "
                       f"胜率={row['validate_win_rate']:.1f}%, "
                       f"回撤={row['validate_max_drawdown']:.1f}%")
    
    # 使用最优参数运行BulletTrade完整回测验证
    logger.info("\n" + "-" * 70)
    logger.info("使用最优参数运行BulletTrade完整回测验证")
    
    try:
        # 验证集完整回测
        full_result = run_bullettrade_backtest(
            best_params,
            validate_period[0],
            validate_period[1],
        )
        
        if not full_result.error:
            logger.info(f"✅ BulletTrade验证结果:")
            logger.info(f"   总收益: {full_result.total_return:.2f}%")
            logger.info(f"   年化收益: {full_result.annual_return:.2f}%")
            logger.info(f"   夏普比率: {full_result.sharpe_ratio:.2f}")
            logger.info(f"   最大回撤: {full_result.max_drawdown:.2f}%")
            logger.info(f"   胜率: {full_result.win_rate:.2f}%")
        else:
            logger.warning(f"⚠️ BulletTrade验证失败: {full_result.error}")
    
    except Exception as e:
        logger.warning(f"⚠️ BulletTrade验证异常: {e}")
    
    # 总结
    total_time = time.time() - start_time
    logger.info("\n" + "=" * 70)
    logger.info(f"✅ 优化完成! 总用时: {total_time/60:.1f}分钟")
    logger.info("=" * 70)


if __name__ == '__main__':
    main()
