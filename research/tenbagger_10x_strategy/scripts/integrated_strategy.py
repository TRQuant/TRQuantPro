#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
集成版十倍股策略 - 整合市场环境+十倍股评分
"""

import sys
sys.path.insert(0, "/home/taotao/dev/QuantTest/TRQuant")

import json
import logging
import numpy as np
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# 导入模块
from core.market_regime.comprehensive_regime_detector import (
    ComprehensiveRegimeDetector, MarketRegime
)
from core.tenbagger.tenbagger_scorer import TenbaggerScorer, TenbaggerStage


class IntegratedStrategy:
    """集成版十倍股策略"""
    
    def __init__(self):
        self.regime_detector = ComprehensiveRegimeDetector()
        self.tenbagger_scorer = TenbaggerScorer()
        
        # 参数
        self.initial_capital = 1_000_000
        self.max_holdings = 3
        
        # 仓位映射
        self.regime_position = {
            MarketRegime.BULL: 0.90,
            MarketRegime.RECOVERY: 0.75,
            MarketRegime.VOLATILE: 0.50,
            MarketRegime.DISTRIBUTION: 0.30,
            MarketRegime.BEAR: 0.10
        }
        
        self.jq = None
    
    def _ensure_jqdata(self):
        if self.jq is None:
            import jqdatasdk as jq
            with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
                config = json.load(f)
            jq.auth(config['username'], config['password'])
            self.jq = jq
            logger.info(f"✅ JQData: {config['username']}")
    
    def run_backtest(self, start_date: str = "2024-01-01", end_date: str = "2024-12-31"):
        """运行回测"""
        print("="*60)
        print("🎯 集成版十倍股策略回测")
        print("="*60)
        
        self._ensure_jqdata()
        
        # 获取交易日
        trade_days = self.jq.get_trade_days(start_date=start_date, end_date=end_date)
        logger.info(f"📅 回测: {start_date} ~ {end_date}, {len(trade_days)}个交易日")
        
        # 获取股票池
        stocks = list(self.jq.get_index_stocks('000300.XSHG'))[:50]  # 沪深300前50只
        logger.info(f"📊 股票池: {len(stocks)}只")
        
        # 获取价格数据
        logger.info("📥 获取价格数据...")
        price_data = {}
        for stock in stocks:
            df = self.jq.get_price(stock, start_date=start_date, end_date=end_date, 
                                  fields=['close'])
            if df is not None and len(df) > 0:
                price_data[stock] = df['close']
        
        # 回测状态
        equity = self.initial_capital
        positions = {}  # {stock: {'shares': n, 'cost': p}}
        current_regime = None
        base_position = 0.5
        
        logger.info("\n📈 回测进度:")
        
        for i, td in enumerate(trade_days):
            date_str = td.strftime("%Y-%m-%d") if hasattr(td, 'strftime') else str(td)
            
            # 每月检测市场环境
            if i % 20 == 0:
                try:
                    result = self.regime_detector.detect(date_str)
                    regime = result.regime
                    if regime != current_regime:
                        current_regime = regime
                        base_position = self.regime_position.get(regime, 0.5)
                        logger.info(f"📊 [{date_str}] 环境: {regime.value:12} 仓位: {base_position*100:.0f}%")
                except:
                    pass
            
            # 计算持仓市值
            portfolio_value = equity
            for stock, pos in positions.items():
                if stock in price_data and date_str in price_data[stock].index:
                    price = price_data[stock].loc[date_str]
                    portfolio_value += pos['shares'] * price
            
            # 每月选股
            if i % 20 == 0 and i > 20:
                # 使用十倍股评分选股
                scored = []
                for stock in stocks:
                    try:
                        score_result = self.tenbagger_scorer.score_stock(stock, date_str)
                        # 优先S1启动期
                        weight = self.tenbagger_scorer.get_stage_weight(score_result.stage)
                        scored.append((stock, score_result.score * weight, score_result.stage))
                    except:
                        pass
                
                # 选择得分最高的股票
                scored.sort(key=lambda x: x[1], reverse=True)
                top_stocks = scored[:self.max_holdings]
                
                # 调仓
                target_value = portfolio_value * base_position
                per_stock = target_value / len(top_stocks) if top_stocks else 0
                
                # 清仓
                for stock in list(positions.keys()):
                    if stock not in [s[0] for s in top_stocks]:
                        if stock in price_data and date_str in price_data[stock].index:
                            price = price_data[stock].loc[date_str]
                            equity += positions[stock]['shares'] * price
                        del positions[stock]
                
                # 买入
                for stock, score, stage in top_stocks:
                    if stock not in positions and stock in price_data:
                        if date_str in price_data[stock].index:
                            price = price_data[stock].loc[date_str]
                            shares = int(per_stock / price / 100) * 100
                            if shares > 0 and equity >= shares * price:
                                positions[stock] = {'shares': shares, 'cost': price}
                                equity -= shares * price
                                logger.info(f"   买入 {stock} @{price:.2f} x{shares} [{stage.value}]")
            
            # 记录净值
            if i % 40 == 0:
                total = equity + sum(
                    pos['shares'] * price_data[s].loc[date_str] 
                    for s, pos in positions.items() 
                    if s in price_data and date_str in price_data[s].index
                )
                ret = (total / self.initial_capital - 1) * 100
                logger.info(f"💰 [{date_str}] 净值: {total:,.0f} 收益: {ret:+.1f}%")
        
        # 最终结果
        final_value = equity
        for stock, pos in positions.items():
            if stock in price_data:
                final_value += pos['shares'] * price_data[stock].iloc[-1]
        
        total_return = (final_value / self.initial_capital - 1) * 100
        
        print("\n" + "="*60)
        print("📋 回测结果")
        print("="*60)
        print(f"初始资金: {self.initial_capital:>15,}")
        print(f"最终净值: {final_value:>15,.0f}")
        print(f"总收益率: {total_return:>14.1f}%")
        
        # 两年5倍评估
        print("\n🎯 两年5倍评估:")
        factor = 1 + total_return/100
        print(f"   一年: {factor:.2f}x")
        print(f"   两年预测: {factor**2:.2f}x")
        print(f"   目标: 5.0x ({factor**2/5*100:.0f}%)")
        
        return total_return


if __name__ == "__main__":
    strategy = IntegratedStrategy()
    strategy.run_backtest()
