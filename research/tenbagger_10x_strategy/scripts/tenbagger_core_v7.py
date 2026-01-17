#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股核心策略 V7.0 - 基于历史案例与早期识别
==============================================

核心理念：
1. 十倍股 = 市场主线 × 早期阶段(S1-S2) × 业绩拐点 × 长期持有
2. 关键是找到S1-S2阶段的潜力股，在市场主线启动时介入
3. 持有周期2-3年，不频繁交易

知识库整合：
- tenbagger_core_strategy_kb.py: 历史案例与买卖规则
- tenbagger_identification_kb.py: 阶段识别与评分
- astock_regime_knowledge_v2.py: 市场环境判断
- strategy_switching_kb.py: 策略切换逻辑

与之前版本的区别：
- V4-V6: 基于技术指标的短线交易，月度调仓
- V7: 基于基本面的长线投资，季度调仓，专注S1-S2阶段

创建时间：2025-12-27
"""

import sys
import os
import logging
import argparse
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import pandas as pd
import numpy as np

# 添加项目根目录
sys.path.insert(0, '/home/taotao/dev/QuantTest/TRQuant')

# 导入知识库
from research.tenbagger_10x_strategy.knowledge.tenbagger_core_strategy_kb import (
    HISTORICAL_TENBAGGERS,
    TenbaggerEarlySignals,
    TENBAGGER_BUY_RULES,
    TENBAGGER_SELL_RULES,
    STAGE_POSITION_STRATEGY,
    EarlyEntryAlgorithm,
)
from research.tenbagger_10x_strategy.knowledge.tenbagger_identification_kb import (
    TenbaggerStage,
    TenbaggerIdentifier,
    TenbaggerScorer,
    STAGE_CHARACTERISTICS,
)
from research.tenbagger_10x_strategy.knowledge.astock_regime_knowledge_v2 import (
    AStockRegime,
    AStockRegimeDetectorV2,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TenbaggerCoreStrategyV7:
    """十倍股核心策略 V7
    
    核心逻辑：
    1. 筛选候选池：市值30-500亿，利润增速>20%，处于S1-S2阶段
    2. 早期进入：使用EarlyEntryAlgorithm评分，>=65分介入
    3. 阶段化持仓：S1小仓位，S2加仓，S3持有，S4减仓，S5退出
    4. 长周期持有：最小持有3个月，目标持有1-2年
    5. 动态止盈：3倍卖20%，5倍卖30%，10倍卖50%
    """
    
    def __init__(self, initial_capital: float = 1_000_000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}  # {stock_code: {'shares': n, 'avg_cost': p, 'entry_date': d, 'stage': s}}
        self.trades = []
        self.daily_values = []
        
        # 知识库
        self.early_signals = TenbaggerEarlySignals()
        self.identifier = TenbaggerIdentifier()
        self.regime_detector = AStockRegimeDetectorV2()
        
        # JQData认证
        self._ensure_jqdata_auth()
        
        # 预加载数据
        self.price_data = None
        self.fundamental_data = None
        
    def _ensure_jqdata_auth(self):
        """确保JQData认证"""
        try:
            import jqdatasdk as jq
            jq.auth('13327806797', 'Taorui888')
            logger.info("JQData认证成功")
        except Exception as e:
            logger.error(f"JQData认证失败: {e}")
            raise
    
    def _preload_data(self, start_date: str, end_date: str):
        """预加载所有需要的数据"""
        import jqdatasdk as jq
        
        logger.info(f"预加载数据: {start_date} ~ {end_date}")
        
        # 获取交易日
        self.trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        
        # 获取股票列表（排除ST、新股）
        all_stocks = jq.get_all_securities(types=['stock'], date=start_date)
        
        # 过滤条件
        valid_stocks = all_stocks[
            ~all_stocks['display_name'].str.contains('ST') &
            (all_stocks['start_date'] < pd.to_datetime(start_date) - timedelta(days=365))
        ].index.tolist()
        
        logger.info(f"候选股票数: {len(valid_stocks)}")
        
        # 获取价格数据
        self.price_data = jq.get_price(
            valid_stocks,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['open', 'close', 'high', 'low', 'volume', 'money'],
            panel=False
        )
        
        if self.price_data is not None:
            self.price_data['date'] = pd.to_datetime(self.price_data['time']).dt.date
            logger.info(f"价格数据加载: {len(self.price_data)} 条")
        
        # 获取财务数据（季度更新）
        self._load_fundamental_data(valid_stocks, start_date)
    
    def _load_fundamental_data(self, stocks: List[str], date: str):
        """加载财务基本面数据"""
        import jqdatasdk as jq
        
        logger.info("加载财务数据...")
        
        try:
            # 获取最新财务指标
            q = jq.query(
                jq.valuation.code,
                jq.valuation.market_cap,
                jq.valuation.pe_ratio,
                jq.indicator.roe,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin,
            ).filter(
                jq.valuation.code.in_(stocks[:500])  # 限制数量
            )
            
            self.fundamental_data = jq.get_fundamentals(q, date=date)
            
            if self.fundamental_data is not None:
                self.fundamental_data = self.fundamental_data.set_index('code')
                logger.info(f"财务数据加载: {len(self.fundamental_data)} 只股票")
            
        except Exception as e:
            logger.warning(f"财务数据加载失败: {e}")
            self.fundamental_data = pd.DataFrame()
    
    def _screen_candidates(self, date: str) -> List[Dict]:
        """筛选十倍股候选
        
        基于知识库的筛选条件：
        1. 市值: 30-500亿
        2. 利润增速: >20%
        3. 营收增速: >15%
        4. ROE: >5%
        5. 估计阶段: S1-S2
        """
        if self.fundamental_data is None or len(self.fundamental_data) == 0:
            return []
        
        candidates = []
        
        for code, row in self.fundamental_data.iterrows():
            try:
                market_cap = row.get('market_cap', 0) or 0
                pe = row.get('pe_ratio', 0) or 0
                roe = row.get('roe', 0) or 0
                revenue_growth = (row.get('inc_revenue_year_on_year', 0) or 0) / 100
                profit_growth = (row.get('inc_net_profit_year_on_year', 0) or 0) / 100
                gross_margin = (row.get('gross_profit_margin', 0) or 0) / 100
                
                # 基础筛选
                if not (self.early_signals.acceptable_market_cap_range[0] <= market_cap <= self.early_signals.acceptable_market_cap_range[1]):
                    continue
                
                if profit_growth < self.early_signals.min_profit_growth:
                    continue
                
                if revenue_growth < self.early_signals.min_revenue_growth:
                    continue
                
                if roe < self.early_signals.min_roe:
                    continue
                
                # 识别阶段
                stage = self.identifier.identify_stage(
                    market_cap=market_cap,
                    revenue_growth=revenue_growth,
                    profit_growth=profit_growth,
                    roe=roe / 100 if roe > 1 else roe
                )
                
                # 只要S0-S3阶段（排除成熟期和衰退期）
                if stage in [TenbaggerStage.S4_MATURITY, TenbaggerStage.S5_DECLINE]:
                    continue
                
                # 计算十倍股评分
                is_potential, score, _, details = self.identifier.is_potential_tenbagger(
                    roe=roe / 100 if roe > 1 else roe,
                    gross_margin=gross_margin,
                    net_margin=0.1,  # 默认值
                    debt_ratio=0.4,  # 默认值
                    revenue_growth=revenue_growth,
                    profit_growth=profit_growth,
                    peg=pe / (profit_growth * 100 + 1) if profit_growth > 0 else 99,
                    pe=pe,
                    market_cap=market_cap,
                    momentum_20d=0.05,  # 默认值
                    volume_ratio=1.2,  # 默认值
                    price_position=0.5,  # 默认值
                )
                
                candidates.append({
                    'code': code,
                    'market_cap': market_cap,
                    'pe': pe,
                    'roe': roe,
                    'revenue_growth': revenue_growth,
                    'profit_growth': profit_growth,
                    'gross_margin': gross_margin,
                    'stage': stage.value,
                    'score': score,
                    'is_potential': is_potential,
                    'details': details,
                })
                
            except Exception as e:
                continue
        
        # 按得分排序
        candidates.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f"筛选出 {len(candidates)} 只候选股票")
        return candidates
    
    def _calculate_entry_score(self, candidate: Dict) -> Tuple[float, str]:
        """计算早期进入得分"""
        score, details, advice = EarlyEntryAlgorithm.calculate_entry_score(
            stage=candidate['stage'].split('_')[0] if '_' in candidate['stage'] else candidate['stage'][:2],
            market_cap=candidate['market_cap'],
            revenue_growth=candidate['revenue_growth'],
            profit_growth=candidate['profit_growth'],
            prev_profit_growth=candidate['profit_growth'] * 0.8,  # 假设上季度增速
            mainline_score=70,  # 默认主线得分
            research_report_count=5,  # 默认研报数
            institution_ratio=0.15,  # 默认机构持仓
            has_catalyst=candidate['profit_growth'] > 0.5,  # 高增长视为催化剂
            technical_breakout=False,
        )
        return score, advice
    
    def _get_stage_position_limit(self, stage: str) -> float:
        """获取阶段对应的持仓上限"""
        stage_key = stage.split('_')[0] if '_' in stage else stage[:2]
        strategy = STAGE_POSITION_STRATEGY.get(stage_key, STAGE_POSITION_STRATEGY['S0'])
        return strategy['max_position']
    
    def _execute_trades(self, date, candidates: List[Dict]):
        """执行交易"""
        import jqdatasdk as jq
        
        # 获取当日价格
        date_str = date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)
        
        # 卖出检查（优先处理）
        positions_to_sell = []
        for code, pos in list(self.positions.items()):
            # 获取当前价格
            try:
                price_row = self.price_data[
                    (self.price_data['code'] == code) & 
                    (self.price_data['date'] == pd.to_datetime(date_str).date())
                ]
                if price_row.empty:
                    continue
                current_price = price_row['close'].values[0]
            except:
                continue
            
            # 计算收益率
            return_rate = (current_price - pos['avg_cost']) / pos['avg_cost']
            
            # 检查卖出条件
            should_sell = False
            sell_ratio = 0
            sell_reason = ""
            
            # 规则1：阶段成熟（S5）
            if pos['stage'].startswith('S5') or pos['stage'] == 'S5_DECLINE':
                should_sell = True
                sell_ratio = 1.0
                sell_reason = "阶段成熟-全部卖出"
            
            # 规则2：目标达成
            elif return_rate >= 10.0:  # 10倍
                sell_ratio = 0.50
                sell_reason = "涨10倍-卖50%"
                should_sell = True
            elif return_rate >= 5.0:  # 5倍
                sell_ratio = 0.30
                sell_reason = "涨5倍-卖30%"
                should_sell = True
            elif return_rate >= 3.0:  # 3倍
                sell_ratio = 0.20
                sell_reason = "涨3倍-卖20%"
                should_sell = True
            
            # 规则3：止损
            elif return_rate < -0.20:  # 亏损20%
                should_sell = True
                sell_ratio = 1.0
                sell_reason = "止损-全部卖出"
            
            if should_sell and sell_ratio > 0:
                positions_to_sell.append((code, sell_ratio, current_price, sell_reason))
        
        # 执行卖出
        for code, ratio, price, reason in positions_to_sell:
            pos = self.positions[code]
            shares_to_sell = int(pos['shares'] * ratio)
            if shares_to_sell > 0:
                sell_value = shares_to_sell * price
                self.capital += sell_value
                pos['shares'] -= shares_to_sell
                
                self.trades.append({
                    'date': date_str,
                    'code': code,
                    'action': 'SELL',
                    'shares': shares_to_sell,
                    'price': price,
                    'value': sell_value,
                    'reason': reason,
                })
                
                logger.info(f"[{date_str}] 卖出 {code}: {shares_to_sell}股 @ {price:.2f}, 原因: {reason}")
                
                if pos['shares'] <= 0:
                    del self.positions[code]
        
        # 买入检查
        available_capital = self.capital * 0.9  # 保留10%现金
        max_positions = 10  # 最多持有10只
        
        if len(self.positions) >= max_positions:
            return
        
        # 筛选符合条件的候选
        buy_candidates = []
        for c in candidates[:30]:  # 只看前30名
            entry_score, advice = self._calculate_entry_score(c)
            if entry_score >= EarlyEntryAlgorithm.ENTRY_THRESHOLD:
                if c['code'] not in self.positions:
                    buy_candidates.append({
                        **c,
                        'entry_score': entry_score,
                        'advice': advice,
                    })
        
        # 执行买入
        for c in buy_candidates[:5]:  # 每次最多买5只
            if len(self.positions) >= max_positions:
                break
            
            code = c['code']
            stage = c['stage']
            
            # 获取价格
            try:
                price_row = self.price_data[
                    (self.price_data['code'] == code) & 
                    (self.price_data['date'] == pd.to_datetime(date_str).date())
                ]
                if price_row.empty:
                    continue
                price = price_row['close'].values[0]
            except:
                continue
            
            # 计算买入金额（按阶段确定仓位）
            position_limit = self._get_stage_position_limit(stage)
            target_value = self.initial_capital * position_limit
            actual_value = min(target_value, available_capital / 5)  # 分散投资
            
            if actual_value < 10000:  # 最小买入1万
                continue
            
            shares = int(actual_value / price / 100) * 100  # 整百股
            if shares <= 0:
                continue
            
            cost = shares * price
            if cost > self.capital:
                continue
            
            # 执行买入
            self.capital -= cost
            available_capital -= cost
            
            self.positions[code] = {
                'shares': shares,
                'avg_cost': price,
                'entry_date': date_str,
                'stage': stage,
                'entry_score': c['entry_score'],
            }
            
            self.trades.append({
                'date': date_str,
                'code': code,
                'action': 'BUY',
                'shares': shares,
                'price': price,
                'value': cost,
                'reason': f"早期进入-{c['advice']}-Score:{c['entry_score']:.0f}",
            })
            
            logger.info(f"[{date_str}] 买入 {code}: {shares}股 @ {price:.2f}, 阶段:{stage}, 得分:{c['entry_score']:.0f}")
    
    def _calculate_portfolio_value(self, date) -> float:
        """计算组合价值"""
        date_str = date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)
        
        total_value = self.capital
        
        for code, pos in self.positions.items():
            try:
                price_row = self.price_data[
                    (self.price_data['code'] == code) & 
                    (self.price_data['date'] == pd.to_datetime(date_str).date())
                ]
                if price_row.empty:
                    # 使用成本价
                    price = pos['avg_cost']
                else:
                    price = price_row['close'].values[0]
                
                total_value += pos['shares'] * price
            except:
                total_value += pos['shares'] * pos['avg_cost']
        
        return total_value
    
    def run_backtest(self, start_date: str, end_date: str) -> Dict:
        """运行回测"""
        logger.info(f"开始回测: {start_date} ~ {end_date}")
        
        # 预加载数据
        self._preload_data(start_date, end_date)
        
        if self.price_data is None or len(self.price_data) == 0:
            logger.error("无法加载价格数据")
            return {"success": False, "error": "数据加载失败"}
        
        # 按季度调仓（每3个月）
        rebalance_interval = 60  # 约60个交易日
        last_rebalance = 0
        
        for i, date in enumerate(self.trade_days):
            date_str = date.strftime('%Y-%m-%d') if hasattr(date, 'strftime') else str(date)
            
            # 每60个交易日重新筛选和调仓
            if i - last_rebalance >= rebalance_interval or i == 0:
                # 更新财务数据
                valid_stocks = self.price_data['code'].unique().tolist()
                self._load_fundamental_data(valid_stocks[:500], date_str)
                
                # 筛选候选
                candidates = self._screen_candidates(date_str)
                
                # 执行交易
                self._execute_trades(date, candidates)
                
                last_rebalance = i
            else:
                # 非调仓日只检查卖出条件
                self._execute_trades(date, [])
            
            # 记录每日净值
            daily_value = self._calculate_portfolio_value(date)
            self.daily_values.append({
                'date': date_str,
                'value': daily_value,
                'positions': len(self.positions),
            })
            
            # 进度显示
            if i % 50 == 0:
                logger.info(f"进度: {i+1}/{len(self.trade_days)}, 净值: {daily_value/self.initial_capital:.2%}")
        
        # 计算结果
        return self._calc_result()
    
    def _calc_result(self) -> Dict:
        """计算回测结果"""
        if not self.daily_values:
            return {"success": False, "error": "无交易数据"}
        
        df = pd.DataFrame(self.daily_values)
        df['return'] = df['value'] / self.initial_capital - 1
        
        final_value = df['value'].iloc[-1]
        total_return = (final_value / self.initial_capital - 1) * 100
        
        # 计算年化收益
        days = len(df)
        annual_return = ((final_value / self.initial_capital) ** (252 / days) - 1) * 100 if days > 0 else 0
        
        # 计算最大回撤
        df['cummax'] = df['value'].cummax()
        df['drawdown'] = (df['cummax'] - df['value']) / df['cummax']
        max_drawdown = df['drawdown'].max() * 100
        
        # 计算夏普比率
        df['daily_return'] = df['value'].pct_change()
        sharpe = df['daily_return'].mean() / df['daily_return'].std() * np.sqrt(252) if df['daily_return'].std() > 0 else 0
        
        result = {
            "success": True,
            "initial_capital": self.initial_capital,
            "final_value": final_value,
            "total_return": total_return,
            "annual_return": annual_return,
            "max_drawdown": max_drawdown,
            "sharpe_ratio": sharpe,
            "total_trades": len(self.trades),
            "final_positions": len(self.positions),
            "trades": self.trades[-20:],  # 最近20笔交易
        }
        
        logger.info("=" * 60)
        logger.info(f"回测结果:")
        logger.info(f"  总收益率: {total_return:.2f}%")
        logger.info(f"  年化收益: {annual_return:.2f}%")
        logger.info(f"  最大回撤: {max_drawdown:.2f}%")
        logger.info(f"  夏普比率: {sharpe:.2f}")
        logger.info(f"  交易次数: {len(self.trades)}")
        logger.info("=" * 60)
        
        return result


def main():
    parser = argparse.ArgumentParser(description='十倍股核心策略V7回测')
    parser.add_argument('-p', '--period', type=str, default='1y',
                        help='回测周期: 1m/3m/6m/1y/2y/3y')
    parser.add_argument('--start', type=str, help='开始日期 YYYY-MM-DD')
    parser.add_argument('--end', type=str, help='结束日期 YYYY-MM-DD')
    args = parser.parse_args()
    
    # 计算日期范围
    end_date = args.end or '2024-12-20'
    
    period_days = {
        '1m': 30,
        '3m': 90,
        '6m': 180,
        '1y': 365,
        '2y': 730,
        '3y': 1095,
    }
    
    days = period_days.get(args.period, 365)
    start_date = args.start or (datetime.strptime(end_date, '%Y-%m-%d') - timedelta(days=days)).strftime('%Y-%m-%d')
    
    logger.info(f"十倍股核心策略V7 回测")
    logger.info(f"周期: {args.period} ({start_date} ~ {end_date})")
    
    # 运行回测
    strategy = TenbaggerCoreStrategyV7(initial_capital=1_000_000)
    result = strategy.run_backtest(start_date, end_date)
    
    if result['success']:
        print(f"\n{'='*60}")
        print(f"十倍股核心策略V7 回测结果 ({args.period})")
        print(f"{'='*60}")
        print(f"总收益率:   {result['total_return']:.2f}%")
        print(f"年化收益:   {result['annual_return']:.2f}%")
        print(f"最大回撤:   {result['max_drawdown']:.2f}%")
        print(f"夏普比率:   {result['sharpe_ratio']:.2f}")
        print(f"交易次数:   {result['total_trades']}")
        print(f"{'='*60}")
    else:
        print(f"回测失败: {result.get('error', '未知错误')}")


if __name__ == '__main__':
    main()

