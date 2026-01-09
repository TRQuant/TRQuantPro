#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
早期识别系统回测验证

验证思路：
1. 在2024年6月1日使用阶段识别系统筛选出不同阶段的股票
2. 设计多种交易策略
3. 用2024年6月至今的数据验证回报率
4. 多维度比较，找出最佳策略

数据获取规则：基本面指标直接从聚宽数据库获取，不需要单独获取财报
"""

import sys
import os

# 工作目录：/home/taotao/.cursor/worktrees/TRQuant/ope
# 项目根目录：/home/taotao/.cursor/worktrees/TRQuant/ope
PROJECT_ROOT = '/home/taotao/.cursor/worktrees/TRQuant/ope'
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

# 聚宽SDK
import jqdatasdk as jq
from jqdata.client import JQDataClient
from jqdata.auth import authenticate

# 阶段识别
from research.tenbagger_10x_strategy.knowledge.tenbagger_identification_kb import (
    TenbaggerIdentifier, TenbaggerStage, TenbaggerCriteria
)


# ============================================================
# 数据结构定义
# ============================================================

@dataclass
class StockScreenResult:
    """筛选结果"""
    code: str
    name: str
    stage: TenbaggerStage
    score: float
    market_cap: float          # 亿元
    revenue_growth: float      # 营收增速
    profit_growth: float       # 利润增速
    roe: float
    pe: float
    details: Dict = field(default_factory=dict)


@dataclass
class BacktestResult:
    """回测结果"""
    strategy_name: str
    total_return: float        # 总收益率
    annual_return: float       # 年化收益率
    max_drawdown: float        # 最大回撤
    sharpe_ratio: float        # 夏普比率
    win_rate: float            # 胜率
    trade_count: int           # 交易次数
    stocks: List[str]          # 持仓股票
    stage_distribution: Dict   # 阶段分布
    daily_returns: List[float] = field(default_factory=list)


# ============================================================
# 阶段筛选模块
# ============================================================

class StageScreener:
    """阶段筛选器
    
    使用聚宽数据库获取基本面指标，识别股票所处阶段
    """
    
    def __init__(self):
        self.jq_client = JQDataClient()
        self.identifier = TenbaggerIdentifier()
        self._ensure_authenticated()
    
    def _ensure_authenticated(self):
        """确保已认证"""
        if not self.jq_client.is_authenticated():
            authenticate()
            self.jq_client._authenticated = True
            self.jq_client._detect_permission()
    
    def screen_at_date(self, screen_date: str) -> Dict[TenbaggerStage, List[StockScreenResult]]:
        """在指定日期筛选股票并按阶段分组
        
        Args:
            screen_date: 筛选日期，如 '2024-06-01'
            
        Returns:
            按阶段分组的股票结果
        """
        print(f"\n{'='*60}")
        print(f"在 {screen_date} 筛选股票...")
        print(f"{'='*60}")
        
        # 1. 获取所有A股
        all_stocks = jq.get_all_securities(types=['stock'], date=screen_date)
        print(f"获取到 {len(all_stocks)} 只股票")
        
        # 过滤：排除ST、退市、科创板、北交所
        valid_stocks = all_stocks[
            ~all_stocks['display_name'].str.contains('ST|退', na=False) &
            ~all_stocks.index.str.startswith('688') &  # 科创板
            ~all_stocks.index.str.startswith('8')      # 北交所
        ]
        print(f"过滤后剩余 {len(valid_stocks)} 只股票")
        
        # 2. 获取基本面数据（直接从聚宽获取，不需要单独获取财报）
        print("获取基本面指标...")
        fundamentals = self._get_fundamentals(valid_stocks.index.tolist(), screen_date)
        print(f"获取到 {len(fundamentals)} 条基本面数据")
        
        # 3. 获取技术指标
        print("计算技术指标...")
        technicals = self._get_technicals(valid_stocks.index.tolist(), screen_date)
        
        # 4. 识别阶段并筛选
        print("识别股票阶段...")
        results_by_stage: Dict[TenbaggerStage, List[StockScreenResult]] = {
            stage: [] for stage in TenbaggerStage
        }
        
        processed = 0
        for code in fundamentals.index:
            try:
                fund = fundamentals.loc[code]
                tech = technicals.get(code, {})
                
                # 基本数据
                # 注意：聚宽的 market_cap 单位已经是亿元，不需要转换
                market_cap = fund.get('market_cap', 0)
                revenue_growth = fund.get('inc_revenue_year_on_year', 0) / 100 if pd.notna(fund.get('inc_revenue_year_on_year')) else 0
                profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
                roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
                pe = fund.get('pe_ratio', 0) if pd.notna(fund.get('pe_ratio')) else 0
                gross_margin = fund.get('gross_profit_margin', 0) / 100 if pd.notna(fund.get('gross_profit_margin')) else 0
                net_margin = fund.get('net_profit_margin', 0) / 100 if pd.notna(fund.get('net_profit_margin')) else 0
                debt_ratio = fund.get('total_liability', 0) / fund.get('total_assets', 1) if fund.get('total_assets', 0) > 0 else 0
                
                # 技术指标
                momentum_20d = tech.get('momentum_20d', 0)
                volume_ratio = tech.get('volume_ratio', 1)
                price_position = tech.get('price_position', 0.5)
                
                # 基本筛选条件
                if market_cap < 20 or market_cap > 2000:  # 20亿-2000亿
                    continue
                if pe <= 0 or pe > 200:  # 有效PE
                    continue
                    
                # 计算PEG
                peg = pe / (profit_growth * 100) if profit_growth > 0.05 else 10
                
                # 使用TenbaggerIdentifier评估
                is_potential, score, stage, details = self.identifier.is_potential_tenbagger(
                    roe=roe,
                    gross_margin=gross_margin,
                    net_margin=net_margin,
                    debt_ratio=debt_ratio,
                    revenue_growth=revenue_growth,
                    profit_growth=profit_growth,
                    peg=peg,
                    pe=pe,
                    market_cap=market_cap,
                    momentum_20d=momentum_20d,
                    volume_ratio=volume_ratio,
                    price_position=price_position
                )
                
                # 获取股票名称
                name = valid_stocks.loc[code, 'display_name'] if code in valid_stocks.index else code
                
                result = StockScreenResult(
                    code=code,
                    name=name,
                    stage=stage,
                    score=score,
                    market_cap=market_cap,
                    revenue_growth=revenue_growth,
                    profit_growth=profit_growth,
                    roe=roe,
                    pe=pe,
                    details=details
                )
                
                results_by_stage[stage].append(result)
                processed += 1
                
            except Exception as e:
                continue
        
        print(f"成功处理 {processed} 只股票")
        
        # 按得分排序
        for stage in results_by_stage:
            results_by_stage[stage].sort(key=lambda x: x.score, reverse=True)
        
        # 打印统计
        print(f"\n阶段分布统计:")
        for stage, stocks in results_by_stage.items():
            print(f"  {stage.value}: {len(stocks)} 只")
        
        return results_by_stage
    
    def _get_fundamentals(self, codes: List[str], date: str) -> pd.DataFrame:
        """获取基本面数据（直接从聚宽获取）
        
        注意：聚宽的 market_cap 单位是亿元
        """
        try:
            # 分批获取（聚宽限制每次查询数量）
            batch_size = 1000
            all_dfs = []
            
            for i in range(0, len(codes), batch_size):
                batch_codes = codes[i:i+batch_size]
                
                q = jq.query(
                    jq.valuation.code,
                    jq.valuation.market_cap,       # 单位：亿元
                    jq.valuation.pe_ratio,
                    jq.valuation.pb_ratio,
                    jq.indicator.roe,
                    jq.indicator.inc_revenue_year_on_year,
                    jq.indicator.inc_net_profit_year_on_year,
                    jq.indicator.gross_profit_margin,
                    jq.indicator.net_profit_margin,
                    jq.balance.total_assets,
                    jq.balance.total_liability,
                ).filter(
                    jq.valuation.code.in_(batch_codes)
                )
                
                batch_df = jq.get_fundamentals(q, date=date)
                if batch_df is not None and not batch_df.empty:
                    all_dfs.append(batch_df)
            
            if all_dfs:
                df = pd.concat(all_dfs, ignore_index=True)
                df = df.set_index('code')
                return df
            return pd.DataFrame()
            
        except Exception as e:
            print(f"获取基本面数据失败: {e}")
            return pd.DataFrame()
    
    def _get_technicals(self, codes: List[str], date: str) -> Dict[str, Dict]:
        """计算技术指标"""
        result = {}
        
        try:
            # 获取过去60天的价格数据
            start_date = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=90)).strftime('%Y-%m-%d')
            
            # 分批获取（避免数据量过大）
            batch_size = 100
            for i in range(0, len(codes), batch_size):
                batch_codes = codes[i:i+batch_size]
                
                price_df = jq.get_price(
                    batch_codes,
                    start_date=start_date,
                    end_date=date,
                    frequency='daily',
                    fields=['close', 'volume'],
                    panel=False
                )
                
                if price_df is None or price_df.empty:
                    continue
                
                for code in batch_codes:
                    try:
                        stock_data = price_df[price_df['code'] == code].copy()
                        if len(stock_data) < 20:
                            continue
                        
                        closes = stock_data['close'].values
                        volumes = stock_data['volume'].values
                        
                        # 20日动量
                        if len(closes) >= 20:
                            momentum_20d = (closes[-1] / closes[-20] - 1) * 100
                        else:
                            momentum_20d = 0
                        
                        # 量比（5日平均成交量与20日平均成交量之比）
                        if len(volumes) >= 20:
                            vol_5 = np.mean(volumes[-5:])
                            vol_20 = np.mean(volumes[-20:])
                            volume_ratio = vol_5 / vol_20 if vol_20 > 0 else 1
                        else:
                            volume_ratio = 1
                        
                        # 价格位置（当前价格在60日高低点的位置）
                        if len(closes) >= 20:
                            high_60 = np.max(closes[-60:]) if len(closes) >= 60 else np.max(closes)
                            low_60 = np.min(closes[-60:]) if len(closes) >= 60 else np.min(closes)
                            price_position = (closes[-1] - low_60) / (high_60 - low_60) if high_60 > low_60 else 0.5
                        else:
                            price_position = 0.5
                        
                        result[code] = {
                            'momentum_20d': momentum_20d,
                            'volume_ratio': volume_ratio,
                            'price_position': price_position
                        }
                        
                    except Exception:
                        continue
                        
        except Exception as e:
            print(f"获取技术指标失败: {e}")
        
        return result


# ============================================================
# 策略工厂
# ============================================================

class Strategy:
    """策略基类"""
    
    def __init__(self, name: str):
        self.name = name
    
    def select_stocks(
        self, 
        screened: Dict[TenbaggerStage, List[StockScreenResult]]
    ) -> List[Tuple[str, float]]:
        """选择股票和权重
        
        Returns:
            [(code, weight), ...] 权重总和为1
        """
        raise NotImplementedError


class S1OnlyStrategy(Strategy):
    """只买S1萌芽期策略"""
    
    def __init__(self):
        super().__init__("S1单阶段(萌芽期)")
    
    def select_stocks(self, screened):
        stocks = screened.get(TenbaggerStage.S1_EMERGENCE, [])
        # 取得分最高的20只
        top_stocks = stocks[:20]
        if not top_stocks:
            return []
        weight = 1.0 / len(top_stocks)
        return [(s.code, weight) for s in top_stocks]


class S2OnlyStrategy(Strategy):
    """只买S2加速期策略"""
    
    def __init__(self):
        super().__init__("S2单阶段(加速期)")
    
    def select_stocks(self, screened):
        stocks = screened.get(TenbaggerStage.S2_ACCELERATION, [])
        top_stocks = stocks[:20]
        if not top_stocks:
            return []
        weight = 1.0 / len(top_stocks)
        return [(s.code, weight) for s in top_stocks]


class StageWeightStrategy(Strategy):
    """阶段权重策略：S1:20%, S2:50%, S3:30%"""
    
    def __init__(self):
        super().__init__("阶段权重配置")
        self.weights = {
            TenbaggerStage.S1_EMERGENCE: 0.20,
            TenbaggerStage.S2_ACCELERATION: 0.50,
            TenbaggerStage.S3_EXPANSION: 0.30,
        }
    
    def select_stocks(self, screened):
        result = []
        for stage, stage_weight in self.weights.items():
            stocks = screened.get(stage, [])[:10]  # 每个阶段最多10只
            if stocks:
                stock_weight = stage_weight / len(stocks)
                for s in stocks:
                    result.append((s.code, stock_weight))
        return result


class ScoreWeightStrategy(Strategy):
    """得分加权策略：按十倍股得分分配仓位"""
    
    def __init__(self):
        super().__init__("得分加权")
    
    def select_stocks(self, screened):
        # 收集所有潜力股（排除S4、S5）
        candidates = []
        for stage in [TenbaggerStage.S0_SEED, TenbaggerStage.S1_EMERGENCE, 
                      TenbaggerStage.S2_ACCELERATION, TenbaggerStage.S3_EXPANSION]:
            candidates.extend(screened.get(stage, []))
        
        # 按得分排序，取前30只
        candidates.sort(key=lambda x: x.score, reverse=True)
        top_stocks = [s for s in candidates[:30] if s.score >= 50]
        
        if not top_stocks:
            return []
        
        # 按得分分配权重
        total_score = sum(s.score for s in top_stocks)
        return [(s.code, s.score / total_score) for s in top_stocks]


class DynamicRotationStrategy(Strategy):
    """动态轮动策略：月度检查阶段变化并调仓"""
    
    def __init__(self):
        super().__init__("动态轮动")
        self.rebalance_interval = 20  # 交易日
    
    def select_stocks(self, screened):
        # 初始选股：优先S2，其次S1
        candidates = []
        
        # S2优先
        s2_stocks = screened.get(TenbaggerStage.S2_ACCELERATION, [])[:15]
        candidates.extend(s2_stocks)
        
        # S1补充
        s1_stocks = screened.get(TenbaggerStage.S1_EMERGENCE, [])[:10]
        candidates.extend(s1_stocks)
        
        if not candidates:
            return []
        
        weight = 1.0 / len(candidates)
        return [(s.code, weight) for s in candidates]


# ============================================================
# 回测运行器
# ============================================================

class BacktestRunner:
    """回测运行器"""
    
    def __init__(self, initial_capital: float = 1000000):
        self.initial_capital = initial_capital
        self.jq_client = JQDataClient()
        self._ensure_authenticated()
    
    def _ensure_authenticated(self):
        if not self.jq_client.is_authenticated():
            authenticate()
            self.jq_client._authenticated = True
    
    def run(
        self,
        strategy: Strategy,
        stock_weights: List[Tuple[str, float]],
        start_date: str,
        end_date: str,
        screened: Dict[TenbaggerStage, List[StockScreenResult]]
    ) -> BacktestResult:
        """运行回测
        
        Args:
            strategy: 策略对象
            stock_weights: 股票和权重列表
            start_date: 回测开始日期
            end_date: 回测结束日期
            screened: 筛选结果（用于统计阶段分布）
        """
        print(f"\n运行策略: {strategy.name}")
        print(f"  持仓股票: {len(stock_weights)} 只")
        print(f"  回测区间: {start_date} 至 {end_date}")
        
        if not stock_weights:
            return BacktestResult(
                strategy_name=strategy.name,
                total_return=0,
                annual_return=0,
                max_drawdown=0,
                sharpe_ratio=0,
                win_rate=0,
                trade_count=0,
                stocks=[],
                stage_distribution={}
            )
        
        # 获取价格数据
        codes = [s[0] for s in stock_weights]
        weights = {s[0]: s[1] for s in stock_weights}
        
        price_df = jq.get_price(
            codes,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['close'],
            panel=False
        )
        
        if price_df is None or price_df.empty:
            print("  无法获取价格数据")
            return BacktestResult(
                strategy_name=strategy.name,
                total_return=0,
                annual_return=0,
                max_drawdown=0,
                sharpe_ratio=0,
                win_rate=0,
                trade_count=0,
                stocks=codes,
                stage_distribution={}
            )
        
        # 计算每只股票的收益
        stock_returns = {}
        for code in codes:
            stock_data = price_df[price_df['code'] == code]
            if len(stock_data) >= 2:
                start_price = stock_data['close'].iloc[0]
                end_price = stock_data['close'].iloc[-1]
                stock_returns[code] = (end_price - start_price) / start_price
            else:
                stock_returns[code] = 0
        
        # 计算组合收益
        portfolio_return = sum(stock_returns.get(code, 0) * weight 
                               for code, weight in weights.items())
        
        # 计算日收益率（用于夏普比率和最大回撤）
        daily_returns = []
        dates = price_df['time'].unique()
        
        prev_portfolio_value = self.initial_capital
        portfolio_values = [prev_portfolio_value]
        
        for i, date in enumerate(dates):
            if i == 0:
                continue
            
            day_data = price_df[price_df['time'] == date]
            prev_day_data = price_df[price_df['time'] == dates[i-1]]
            
            day_return = 0
            for code, weight in weights.items():
                curr = day_data[day_data['code'] == code]['close']
                prev = prev_day_data[prev_day_data['code'] == code]['close']
                if len(curr) > 0 and len(prev) > 0 and prev.iloc[0] > 0:
                    stock_day_return = (curr.iloc[0] - prev.iloc[0]) / prev.iloc[0]
                    day_return += stock_day_return * weight
            
            daily_returns.append(day_return)
            prev_portfolio_value *= (1 + day_return)
            portfolio_values.append(prev_portfolio_value)
        
        # 计算指标
        # 最大回撤
        max_drawdown = 0
        peak = portfolio_values[0]
        for value in portfolio_values:
            if value > peak:
                peak = value
            drawdown = (peak - value) / peak
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # 夏普比率（假设无风险利率3%）
        if daily_returns:
            daily_rf = 0.03 / 252
            excess_returns = [r - daily_rf for r in daily_returns]
            if np.std(excess_returns) > 0:
                sharpe = np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
            else:
                sharpe = 0
        else:
            sharpe = 0
        
        # 年化收益
        days = len(dates)
        annual_return = (1 + portfolio_return) ** (252 / max(days, 1)) - 1
        
        # 胜率
        win_count = sum(1 for r in stock_returns.values() if r > 0)
        win_rate = win_count / len(stock_returns) if stock_returns else 0
        
        # 阶段分布统计
        stage_dist = {}
        for stage, stocks in screened.items():
            for s in stocks:
                if s.code in codes:
                    stage_dist[stage.value] = stage_dist.get(stage.value, 0) + 1
        
        result = BacktestResult(
            strategy_name=strategy.name,
            total_return=portfolio_return,
            annual_return=annual_return,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe,
            win_rate=win_rate,
            trade_count=len(codes),
            stocks=codes,
            stage_distribution=stage_dist,
            daily_returns=daily_returns
        )
        
        print(f"  总收益: {portfolio_return*100:.2f}%")
        print(f"  年化收益: {annual_return*100:.2f}%")
        print(f"  最大回撤: {max_drawdown*100:.2f}%")
        print(f"  夏普比率: {sharpe:.2f}")
        print(f"  胜率: {win_rate*100:.1f}%")
        
        return result


# ============================================================
# 多维分析模块
# ============================================================

class BacktestAnalyzer:
    """回测结果分析器"""
    
    def __init__(self):
        self.jq_client = JQDataClient()
    
    def compare_strategies(self, results: List[BacktestResult]) -> pd.DataFrame:
        """对比多个策略"""
        data = []
        for r in results:
            data.append({
                '策略': r.strategy_name,
                '总收益%': f"{r.total_return*100:.2f}",
                '年化收益%': f"{r.annual_return*100:.2f}",
                '最大回撤%': f"{r.max_drawdown*100:.2f}",
                '夏普比率': f"{r.sharpe_ratio:.2f}",
                '胜率%': f"{r.win_rate*100:.1f}",
                '持仓数': r.trade_count,
            })
        
        df = pd.DataFrame(data)
        
        # 按总收益排序
        df['_sort'] = df['总收益%'].astype(float)
        df = df.sort_values('_sort', ascending=False).drop('_sort', axis=1)
        
        return df
    
    def validate_stage_predictions(
        self,
        screened_at_start: Dict[TenbaggerStage, List[StockScreenResult]],
        current_date: str
    ) -> Dict:
        """验证阶段预测准确率
        
        对比筛选时的阶段与当前实际阶段
        """
        print(f"\n验证阶段预测准确率（对比 {current_date}）...")
        
        screener = StageScreener()
        identifier = TenbaggerIdentifier()
        
        # 收集所有初始筛选的股票
        all_stocks = {}
        for stage, stocks in screened_at_start.items():
            for s in stocks[:10]:  # 每个阶段取前10只
                all_stocks[s.code] = {
                    'initial_stage': stage,
                    'initial_score': s.score,
                    'name': s.name
                }
        
        if not all_stocks:
            return {'accuracy': 0, 'correct': 0, 'upgraded': 0, 'downgraded': 0, 'total': 0, 'details': []}
        
        # 获取当前基本面数据
        codes = list(all_stocks.keys())
        fundamentals = screener._get_fundamentals(codes, current_date)
        technicals = screener._get_technicals(codes, current_date)
        
        # 计算当前阶段
        results = []
        correct = 0
        upgraded = 0
        downgraded = 0
        
        for code in codes:
            if code not in fundamentals.index:
                continue
            
            fund = fundamentals.loc[code]
            tech = technicals.get(code, {})
            
            market_cap = fund.get('market_cap', 0)  # 聚宽单位已经是亿元
            revenue_growth = fund.get('inc_revenue_year_on_year', 0) / 100 if pd.notna(fund.get('inc_revenue_year_on_year')) else 0
            profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
            roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
            
            # 识别当前阶段
            current_stage = identifier.identify_stage(market_cap, revenue_growth, profit_growth, roe)
            
            initial_stage = all_stocks[code]['initial_stage']
            
            # 阶段顺序
            stage_order = {
                TenbaggerStage.S0_SEED: 0,
                TenbaggerStage.S1_EMERGENCE: 1,
                TenbaggerStage.S2_ACCELERATION: 2,
                TenbaggerStage.S3_EXPANSION: 3,
                TenbaggerStage.S4_MATURITY: 4,
                TenbaggerStage.S5_DECLINE: 5
            }
            
            initial_order = stage_order[initial_stage]
            current_order = stage_order[current_stage]
            
            if current_order == initial_order:
                status = "保持"
                correct += 1
            elif current_order > initial_order:
                if current_stage in [TenbaggerStage.S4_MATURITY, TenbaggerStage.S5_DECLINE]:
                    status = "恶化"
                    downgraded += 1
                else:
                    status = "升级"
                    upgraded += 1
            else:
                status = "降级"
                downgraded += 1
            
            results.append({
                'code': code,
                'name': all_stocks[code]['name'],
                'initial_stage': initial_stage.value,
                'current_stage': current_stage.value,
                'status': status
            })
        
        accuracy = correct / len(results) if results else 0
        
        return {
            'accuracy': accuracy,
            'correct': correct,
            'upgraded': upgraded,
            'downgraded': downgraded,
            'total': len(results),
            'details': results
        }
    
    def analyze_stage_returns(
        self,
        screened: Dict[TenbaggerStage, List[StockScreenResult]],
        start_date: str,
        end_date: str
    ) -> pd.DataFrame:
        """分析各阶段股票的平均收益"""
        print(f"\n分析各阶段股票收益...")
        
        stage_returns = {}
        
        for stage, stocks in screened.items():
            if not stocks:
                continue
            
            codes = [s.code for s in stocks[:20]]  # 每个阶段取前20只
            
            if not codes:
                continue
            
            price_df = jq.get_price(
                codes,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['close'],
                panel=False
            )
            
            if price_df is None or price_df.empty:
                continue
            
            returns = []
            for code in codes:
                stock_data = price_df[price_df['code'] == code]
                if len(stock_data) >= 2:
                    start_price = stock_data['close'].iloc[0]
                    end_price = stock_data['close'].iloc[-1]
                    ret = (end_price - start_price) / start_price
                    returns.append(ret)
            
            if returns:
                stage_returns[stage.value] = {
                    'avg_return': np.mean(returns),
                    'max_return': np.max(returns),
                    'min_return': np.min(returns),
                    'win_rate': sum(1 for r in returns if r > 0) / len(returns),
                    'count': len(returns)
                }
        
        # 转为DataFrame
        data = []
        for stage, stats in stage_returns.items():
            data.append({
                '阶段': stage,
                '平均收益%': f"{stats['avg_return']*100:.2f}",
                '最高收益%': f"{stats['max_return']*100:.2f}",
                '最低收益%': f"{stats['min_return']*100:.2f}",
                '胜率%': f"{stats['win_rate']*100:.1f}",
                '样本数': stats['count']
            })
        
        return pd.DataFrame(data)


# ============================================================
# 主验证流程
# ============================================================

def run_validation():
    """运行完整验证流程"""
    
    # 配置
    SCREEN_DATE = '2024-06-01'
    START_DATE = '2024-06-03'  # 第一个交易日
    END_DATE = datetime.now().strftime('%Y-%m-%d')  # 到今天
    
    print("="*70)
    print("早期识别系统回测验证")
    print("="*70)
    print(f"筛选日期: {SCREEN_DATE}")
    print(f"回测区间: {START_DATE} 至 {END_DATE}")
    print("="*70)
    
    # 1. 筛选股票
    screener = StageScreener()
    screened = screener.screen_at_date(SCREEN_DATE)
    
    # 2. 准备策略
    strategies = [
        S1OnlyStrategy(),
        S2OnlyStrategy(),
        StageWeightStrategy(),
        ScoreWeightStrategy(),
        DynamicRotationStrategy(),
    ]
    
    # 3. 运行回测
    runner = BacktestRunner()
    results = []
    
    for strategy in strategies:
        stock_weights = strategy.select_stocks(screened)
        result = runner.run(strategy, stock_weights, START_DATE, END_DATE, screened)
        results.append(result)
    
    # 4. 分析结果
    analyzer = BacktestAnalyzer()
    
    print("\n" + "="*70)
    print("策略对比结果")
    print("="*70)
    comparison = analyzer.compare_strategies(results)
    print(comparison.to_string(index=False))
    
    print("\n" + "="*70)
    print("各阶段股票收益分析")
    print("="*70)
    stage_returns = analyzer.analyze_stage_returns(screened, START_DATE, END_DATE)
    print(stage_returns.to_string(index=False))
    
    print("\n" + "="*70)
    print("阶段预测准确率验证")
    print("="*70)
    prediction_result = analyzer.validate_stage_predictions(screened, END_DATE)
    print(f"准确率: {prediction_result['accuracy']*100:.1f}%")
    print(f"保持: {prediction_result['correct']}, 升级: {prediction_result['upgraded']}, 恶化: {prediction_result['downgraded']}")
    
    # 5. 找出最佳策略
    best_result = max(results, key=lambda x: x.total_return)
    print("\n" + "="*70)
    print(f"最佳策略: {best_result.strategy_name}")
    print(f"总收益: {best_result.total_return*100:.2f}%")
    print(f"夏普比率: {best_result.sharpe_ratio:.2f}")
    print("="*70)
    
    return {
        'screened': screened,
        'results': results,
        'comparison': comparison,
        'stage_returns': stage_returns,
        'prediction': prediction_result,
        'best_strategy': best_result
    }


if __name__ == '__main__':
    run_validation()
