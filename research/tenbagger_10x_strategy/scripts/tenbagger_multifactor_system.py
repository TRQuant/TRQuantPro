#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
十倍股多因子量化系统 - 早期识别与波段操作
==========================================

整合知识库核心逻辑：
1. 阶段识别系统（S0-S5）
2. 7维评分卡
3. 多因子打分模型
4. 科技主线识别
5. 波段操作+回撤控制

目标：聚焦5只以内股票，获取10倍以上回报

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_multifactor_system.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 阶段定义
# ============================================================

class Stage(Enum):
    """十倍股成长阶段"""
    S0 = "S0"  # 观察期 - 有产业链位置，无明显兑现信号
    S1 = "S1"  # 验证期 - 送样/认证中，尚未确认客户
    S2 = "S2"  # 导入期 - 已进入客户体系，最佳介入点
    S3 = "S3"  # 放量期 - 批量订单，扩产明确
    S4 = "S4"  # 加速期 - 业绩拐点，估值修复
    S5 = "S5"  # 成熟期 - 主流共识，十倍股特征消失


STAGE_WEIGHTS = {
    Stage.S0: 0.2,
    Stage.S1: 0.5,
    Stage.S2: 1.0,  # 最佳介入
    Stage.S3: 0.8,
    Stage.S4: 0.4,
    Stage.S5: 0.1,
}


# ============================================================
# 科技主线板块
# ============================================================

TECH_MAINLINE_INDUSTRIES = {
    # AI人工智能
    "AI芯片": ["算力", "GPU", "NPU", "ASIC"],
    "AI算法": ["大模型", "机器学习", "深度学习"],
    "AI应用": ["智能驾驶", "机器人", "具身智能"],
    
    # 半导体
    "半导体设备": ["光刻", "刻蚀", "薄膜沉积", "离子注入"],
    "半导体材料": ["光刻胶", "特种气体", "靶材", "CMP"],
    "芯片设计": ["CPU", "GPU", "存储芯片", "MCU"],
    
    # 新能源
    "锂电池": ["正极材料", "负极材料", "隔膜", "电解液"],
    "光伏": ["硅料", "硅片", "电池片", "组件"],
    "储能": ["储能系统", "逆变器", "BMS"],
    
    # 其他高科技
    "量子计算": ["量子芯片", "量子通信"],
    "生物医药": ["创新药", "CXO", "医疗器械"],
}

TECH_KEYWORDS = [
    "AI", "人工智能", "大模型", "算力", "芯片", "半导体", "GPU", "CPU",
    "机器人", "自动驾驶", "智能驾驶", "新能源", "锂电", "光伏", "储能",
    "量子", "生物医药", "创新药", "5G", "6G", "物联网", "边缘计算"
]


# ============================================================
# 7维评分卡
# ============================================================

@dataclass
class ScorecardResult:
    """评分卡结果"""
    symbol: str
    name: str
    total_score: float
    grade: str
    dimensions: Dict[str, float]
    signals: List[str]


class ScoreCardEngine:
    """7维评分卡引擎"""
    
    # 维度权重
    DIMENSION_WEIGHTS = {
        "profitability": 0.15,      # 盈利能力
        "growth": 0.20,             # 成长性
        "financial_health": 0.10,   # 财务健康
        "valuation": 0.15,          # 估值水平
        "industry_position": 0.15,  # 行业地位
        "management": 0.10,         # 管理质量
        "market_performance": 0.15, # 市场表现
    }
    
    def compute(self, symbol: str, name: str, data: Dict) -> ScorecardResult:
        """计算评分"""
        scores = {}
        signals = []
        
        # 1. 盈利能力
        roe = data.get('roe', 0)
        gross_margin = data.get('gross_margin', 0)
        
        profitability_score = 0
        if roe > 20:
            profitability_score = 100
            signals.append(f"ROE极高({roe:.1f}%)")
        elif roe > 15:
            profitability_score = 80
        elif roe > 10:
            profitability_score = 60
        elif roe > 5:
            profitability_score = 40
        else:
            profitability_score = 20
        
        if gross_margin > 40:
            profitability_score = min(100, profitability_score + 20)
            signals.append(f"毛利率高({gross_margin:.1f}%)")
        
        scores['profitability'] = profitability_score
        
        # 2. 成长性
        revenue_growth = data.get('revenue_growth', 0)
        profit_growth = data.get('profit_growth', 0)
        
        growth_score = 0
        if revenue_growth > 50:
            growth_score = 100
            signals.append(f"营收高增长({revenue_growth:.0f}%)")
        elif revenue_growth > 30:
            growth_score = 80
        elif revenue_growth > 15:
            growth_score = 60
        elif revenue_growth > 0:
            growth_score = 40
        else:
            growth_score = 20
        
        if profit_growth > 50:
            growth_score = min(100, growth_score + 20)
            signals.append(f"利润高增长({profit_growth:.0f}%)")
        
        scores['growth'] = growth_score
        
        # 3. 财务健康
        debt_ratio = data.get('debt_ratio', 50)
        current_ratio = data.get('current_ratio', 1)
        
        health_score = 0
        if debt_ratio < 30:
            health_score = 100
        elif debt_ratio < 50:
            health_score = 80
        elif debt_ratio < 70:
            health_score = 60
        else:
            health_score = 40
        
        if current_ratio > 2:
            health_score = min(100, health_score + 10)
        
        scores['financial_health'] = health_score
        
        # 4. 估值水平
        pe = data.get('pe', 50)
        pb = data.get('pb', 3)
        
        valuation_score = 0
        if 0 < pe < 20:
            valuation_score = 100
            signals.append(f"估值合理(PE={pe:.0f})")
        elif 20 <= pe < 40:
            valuation_score = 70
        elif 40 <= pe < 80:
            valuation_score = 50
        else:
            valuation_score = 30
        
        scores['valuation'] = valuation_score
        
        # 5. 行业地位
        market_share = data.get('market_share', 0)
        is_leader = data.get('is_leader', False)
        
        industry_score = 50  # 默认中等
        if is_leader:
            industry_score = 90
            signals.append("行业龙头")
        elif market_share > 10:
            industry_score = 70
        
        scores['industry_position'] = industry_score
        
        # 6. 管理质量
        rd_ratio = data.get('rd_ratio', 0)  # 研发投入占比
        
        management_score = 50
        if rd_ratio > 10:
            management_score = 90
            signals.append(f"研发投入高({rd_ratio:.1f}%)")
        elif rd_ratio > 5:
            management_score = 70
        
        scores['management'] = management_score
        
        # 7. 市场表现
        momentum_20d = data.get('momentum_20d', 0)
        momentum_60d = data.get('momentum_60d', 0)
        vol_ratio = data.get('vol_ratio', 1)
        
        market_score = 50
        if momentum_20d > 20 and momentum_60d > 30:
            market_score = 90
            signals.append("强势动量")
        elif momentum_20d > 10:
            market_score = 70
        elif momentum_20d < -10:
            market_score = 30
        
        if vol_ratio > 2:
            market_score = min(100, market_score + 10)
            signals.append("放量突破")
        
        scores['market_performance'] = market_score
        
        # 计算总分
        total_score = sum(scores[k] * self.DIMENSION_WEIGHTS[k] for k in scores)
        
        # 确定等级
        if total_score >= 85:
            grade = "S+"
        elif total_score >= 75:
            grade = "S"
        elif total_score >= 65:
            grade = "A"
        elif total_score >= 50:
            grade = "B"
        elif total_score >= 35:
            grade = "C"
        else:
            grade = "D"
        
        return ScorecardResult(
            symbol=symbol,
            name=name,
            total_score=total_score,
            grade=grade,
            dimensions=scores,
            signals=signals
        )


# ============================================================
# 阶段识别引擎
# ============================================================

class StageIdentifier:
    """阶段识别引擎"""
    
    def identify(self, data: Dict) -> Tuple[Stage, float, List[str]]:
        """
        识别股票所处阶段
        
        Returns:
            (阶段, 置信度, 信号列表)
        """
        signals = []
        
        revenue_growth = data.get('revenue_growth', 0)
        profit_growth = data.get('profit_growth', 0)
        momentum_20d = data.get('momentum_20d', 0)
        momentum_60d = data.get('momentum_60d', 0)
        vol_ratio = data.get('vol_ratio', 1)
        pe = data.get('pe', 50)
        market_cap = data.get('market_cap', 100)  # 亿
        
        # S4加速期: 业绩爆发，估值修复
        if revenue_growth > 80 and profit_growth > 100 and momentum_60d > 50:
            signals.append("业绩拐点确认")
            signals.append("估值快速修复")
            return Stage.S4, 0.85, signals
        
        # S3放量期: 批量订单，扩产
        if revenue_growth > 50 and profit_growth > 60 and vol_ratio > 1.5:
            signals.append("营收高速增长")
            signals.append("放量上涨")
            if momentum_20d > 15:
                return Stage.S3, 0.80, signals
        
        # S2导入期 (最佳买点): 小批量验证通过
        if 30 <= revenue_growth <= 60 and 20 <= profit_growth <= 60:
            if momentum_20d > 5 and market_cap < 300:
                signals.append("成长黄金期")
                signals.append("市值适中")
                return Stage.S2, 0.75, signals
        
        # S1验证期: 有增长但未放量
        if 15 <= revenue_growth < 40 and profit_growth > 10:
            signals.append("增长验证中")
            return Stage.S1, 0.60, signals
        
        # S5成熟期: 大市值，低增速
        if market_cap > 1000 and revenue_growth < 15:
            signals.append("增长放缓")
            return Stage.S5, 0.70, signals
        
        # S0观察期
        signals.append("待进一步验证")
        return Stage.S0, 0.40, signals


# ============================================================
# 多因子打分系统
# ============================================================

class MultifactorScorer:
    """多因子打分系统"""
    
    # 因子权重
    FACTOR_WEIGHTS = {
        # 基本面因子 (40%)
        'roe': 0.08,
        'revenue_growth': 0.10,
        'profit_growth': 0.08,
        'gross_margin': 0.06,
        'rd_ratio': 0.08,
        
        # 估值因子 (15%)
        'pe_score': 0.08,
        'pb_score': 0.07,
        
        # 技术因子 (25%)
        'momentum_20d': 0.10,
        'momentum_60d': 0.08,
        'vol_ratio': 0.07,
        
        # 阶段因子 (20%)
        'stage_score': 0.20,
    }
    
    def __init__(self):
        self.stage_identifier = StageIdentifier()
        self.scorecard_engine = ScoreCardEngine()
    
    def score(self, symbol: str, name: str, data: Dict) -> Dict:
        """计算综合得分"""
        
        # 1. 阶段识别
        stage, stage_confidence, stage_signals = self.stage_identifier.identify(data)
        stage_score = STAGE_WEIGHTS.get(stage, 0.2) * 100
        
        # 2. 评分卡
        scorecard = self.scorecard_engine.compute(symbol, name, data)
        
        # 3. 因子得分
        factor_scores = {}
        
        # 基本面因子
        factor_scores['roe'] = min(100, max(0, data.get('roe', 0) * 5))
        factor_scores['revenue_growth'] = min(100, max(0, data.get('revenue_growth', 0) * 2))
        factor_scores['profit_growth'] = min(100, max(0, data.get('profit_growth', 0) * 1.5))
        factor_scores['gross_margin'] = min(100, max(0, data.get('gross_margin', 0) * 2))
        factor_scores['rd_ratio'] = min(100, max(0, data.get('rd_ratio', 0) * 10))
        
        # 估值因子 (低PE/PB得高分)
        pe = data.get('pe', 50)
        factor_scores['pe_score'] = max(0, 100 - pe * 1.5) if pe > 0 else 50
        
        pb = data.get('pb', 3)
        factor_scores['pb_score'] = max(0, 100 - pb * 20) if pb > 0 else 50
        
        # 技术因子
        factor_scores['momentum_20d'] = min(100, max(0, 50 + data.get('momentum_20d', 0) * 2))
        factor_scores['momentum_60d'] = min(100, max(0, 50 + data.get('momentum_60d', 0)))
        factor_scores['vol_ratio'] = min(100, max(0, data.get('vol_ratio', 1) * 40))
        
        # 阶段因子
        factor_scores['stage_score'] = stage_score
        
        # 4. 计算加权总分
        total_score = sum(
            factor_scores.get(k, 50) * self.FACTOR_WEIGHTS[k]
            for k in self.FACTOR_WEIGHTS
        )
        
        # 5. 科技主线加成
        tech_bonus = 0
        industry = data.get('industry', '')
        for keyword in TECH_KEYWORDS:
            if keyword in industry or keyword in name:
                tech_bonus = 10
                break
        
        total_score = min(100, total_score + tech_bonus)
        
        return {
            'symbol': symbol,
            'name': name,
            'total_score': round(total_score, 1),
            'stage': stage.value,
            'stage_confidence': stage_confidence,
            'stage_signals': stage_signals,
            'scorecard_grade': scorecard.grade,
            'scorecard_score': scorecard.total_score,
            'scorecard_signals': scorecard.signals,
            'factor_scores': factor_scores,
            'tech_bonus': tech_bonus,
            'recommendation': self._get_recommendation(total_score, stage)
        }
    
    def _get_recommendation(self, score: float, stage: Stage) -> str:
        """生成推荐"""
        if score >= 80 and stage in [Stage.S1, Stage.S2]:
            return "强烈推荐 - 早期布局良机"
        elif score >= 70 and stage in [Stage.S2, Stage.S3]:
            return "推荐 - 成长黄金期"
        elif score >= 60:
            return "关注 - 等待更好时机"
        elif score >= 50:
            return "观察 - 需更多验证"
        else:
            return "不推荐"


# ============================================================
# 波段操作引擎
# ============================================================

class SwingTradeEngine:
    """波段操作引擎"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.max_holdings = self.config.get('max_holdings', 5)
        self.stop_loss = self.config.get('stop_loss', -0.10)
        self.take_profit = self.config.get('take_profit', 0.50)
        self.trailing_stop = self.config.get('trailing_stop', 0.15)
        self.min_score = self.config.get('min_score', 70)
    
    def generate_signals(self, candidates: List[Dict], current_positions: Dict) -> List[Dict]:
        """
        生成交易信号
        
        Args:
            candidates: 候选股票列表 (已按得分排序)
            current_positions: 当前持仓 {symbol: {shares, cost, highest_price}}
        
        Returns:
            交易信号列表
        """
        signals = []
        
        # 1. 检查卖出信号
        for symbol, pos in current_positions.items():
            cost = pos['cost']
            current_price = pos.get('current_price', cost)
            highest_price = pos.get('highest_price', current_price)
            
            pnl = (current_price - cost) / cost
            drawdown_from_high = (current_price - highest_price) / highest_price if highest_price > 0 else 0
            
            # 止损
            if pnl <= self.stop_loss:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'止损 ({pnl*100:.1f}%)',
                    'priority': 1
                })
                continue
            
            # 止盈
            if pnl >= self.take_profit:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'止盈 ({pnl*100:.1f}%)',
                    'priority': 2
                })
                continue
            
            # 移动止损
            if drawdown_from_high <= -self.trailing_stop:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'移动止损 (从高点回撤 {drawdown_from_high*100:.1f}%)',
                    'priority': 3
                })
        
        # 2. 检查买入信号
        current_count = len(current_positions) - sum(1 for s in signals if s['action'] == 'SELL')
        slots_available = self.max_holdings - current_count
        
        if slots_available > 0:
            for candidate in candidates:
                if len([s for s in signals if s['action'] == 'BUY']) >= slots_available:
                    break
                
                symbol = candidate['symbol']
                
                # 跳过已持有
                if symbol in current_positions:
                    continue
                
                # 检查得分
                if candidate['total_score'] < self.min_score:
                    continue
                
                # 只在S1-S3阶段买入
                stage = candidate.get('stage', 'S0')
                if stage not in ['S1', 'S2', 'S3']:
                    continue
                
                signals.append({
                    'symbol': symbol,
                    'name': candidate.get('name', ''),
                    'action': 'BUY',
                    'reason': f"得分 {candidate['total_score']:.1f}, 阶段 {stage}",
                    'score': candidate['total_score'],
                    'stage': stage,
                    'priority': 10 - int(candidate['total_score'] / 10)  # 高分优先
                })
        
        # 按优先级排序
        signals.sort(key=lambda x: x['priority'])
        
        return signals


# ============================================================
# 主系统
# ============================================================

class TenbaggerMultifactorSystem:
    """十倍股多因子量化系统"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.jqdata_username = self.config.get('jqdata_username', '13327806797')
        self.scorer = MultifactorScorer()
        self.swing_engine = SwingTradeEngine(self.config)
        self.jq_authenticated = False
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth(self.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def get_tech_universe(self) -> List[str]:
        """获取科技主线股票池"""
        # 中证科技100 + 创业板指成分股
        stocks = []
        
        try:
            # 创业板
            stocks += jq.get_index_stocks('399006.XSHE')[:50]
            # 科创50
            stocks += jq.get_index_stocks('000688.XSHG')[:30] if jq.get_index_stocks('000688.XSHG') else []
            # 中证500中的科技股 (通过行业筛选)
            zz500 = jq.get_index_stocks('000905.XSHG')
            
            # 筛选科技行业
            for stock in zz500[:100]:
                try:
                    info = jq.get_security_info(stock)
                    if info and any(kw in info.display_name for kw in TECH_KEYWORDS):
                        stocks.append(stock)
                except:
                    continue
        except:
            pass
        
        return list(set(stocks))
    
    def fetch_stock_data(self, stock: str, date: str) -> Dict:
        """获取股票数据"""
        data = {'symbol': stock}
        
        try:
            # 基本信息
            info = jq.get_security_info(stock)
            if info:
                data['name'] = info.display_name
            
            # 基本面数据
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.market_cap,
                jq.indicator.roe,
                jq.indicator.roa,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin
            ).filter(jq.valuation.code == stock)
            
            fund_df = jq.get_fundamentals(q, date=date)
            
            if not fund_df.empty:
                data['pe'] = fund_df['pe_ratio'].iloc[0] or 50
                data['pb'] = fund_df['pb_ratio'].iloc[0] or 3
                data['market_cap'] = (fund_df['market_cap'].iloc[0] or 100) / 100000000  # 转亿
                data['roe'] = fund_df['roe'].iloc[0] or 0
                data['roa'] = fund_df['roa'].iloc[0] or 0
                data['revenue_growth'] = fund_df['inc_revenue_year_on_year'].iloc[0] or 0
                data['profit_growth'] = fund_df['inc_net_profit_year_on_year'].iloc[0] or 0
                data['gross_margin'] = fund_df['gross_profit_margin'].iloc[0] or 0
            
            # 技术数据
            price_df = jq.get_price(
                stock, end_date=date, count=60,
                frequency='daily', fields=['close', 'volume']
            )
            
            if price_df is not None and len(price_df) >= 60:
                close = price_df['close'].values
                volume = price_df['volume'].values
                
                data['momentum_5d'] = (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0
                data['momentum_20d'] = (close[-1] / close[-20] - 1) * 100 if close[-20] > 0 else 0
                data['momentum_60d'] = (close[-1] / close[0] - 1) * 100 if close[0] > 0 else 0
                data['vol_ratio'] = np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1
                data['current_price'] = close[-1]
            
            # 行业
            try:
                ind = jq.get_industry(stock, date=date)
                if ind and stock in ind:
                    data['industry'] = ind[stock].get('sw_l1', {}).get('industry_name', '')
            except:
                data['industry'] = ''
            
        except Exception as e:
            logger.warning(f"获取{stock}数据失败: {e}")
        
        return data
    
    def scan_and_score(self, date: str = None) -> List[Dict]:
        """扫描并打分"""
        if not self.authenticate_jqdata():
            return []
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📊 开始扫描 ({date})...")
        
        # 获取股票池
        universe = self.get_tech_universe()
        logger.info(f"   股票池: {len(universe)}只")
        
        # 扫描并打分
        results = []
        for i, stock in enumerate(universe):
            if i % 20 == 0:
                logger.info(f"   进度: {i}/{len(universe)}")
            
            data = self.fetch_stock_data(stock, date)
            if data.get('name'):
                score_result = self.scorer.score(stock, data.get('name', ''), data)
                score_result['data'] = data
                results.append(score_result)
        
        # 按得分排序
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        logger.info(f"✅ 扫描完成: {len(results)}只股票")
        
        return results
    
    def get_top_candidates(self, results: List[Dict], top_n: int = 5) -> List[Dict]:
        """获取Top候选"""
        # 只保留S1-S3阶段的高分股票
        filtered = [
            r for r in results
            if r['total_score'] >= 70 and r.get('stage', 'S0') in ['S1', 'S2', 'S3']
        ]
        
        return filtered[:top_n]
    
    def run_backtest(self, start_date: str, end_date: str, initial_capital: float = 1000000) -> Dict:
        """运行回测"""
        if not self.authenticate_jqdata():
            return {'success': False, 'error': 'JQData认证失败'}
        
        logger.info(f"🚀 开始回测: {start_date} ~ {end_date}")
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [str(d) for d in trade_days]
        
        # 获取股票池
        universe = self.get_tech_universe()[:50]  # 限制数量
        
        # 预加载价格数据
        logger.info("   预加载价格数据...")
        price_df = jq.get_price(
            universe,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None:
            for stock in universe:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        # 初始化
        cash = initial_capital
        positions = {}
        equity_curve = [cash]
        trades = []
        
        rebalance_days = self.config.get('rebalance_days', 10)
        counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
            
            # 更新持仓价值和最高价
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    current_price = price_cache[stock].loc[date, 'close']
                    pos['current_price'] = current_price
                    pos['highest_price'] = max(pos.get('highest_price', current_price), current_price)
                    portfolio_value += pos['shares'] * current_price
            
            # 调仓检查
            counter += 1
            if counter >= rebalance_days:
                counter = 0
                
                # 简化版: 基于动量和价格位置打分
                scores = {}
                for stock in universe:
                    if stock in price_cache:
                        try:
                            sdf = price_cache[stock]
                            mask = sdf.index <= date
                            sdf = sdf[mask].tail(60)
                            
                            if len(sdf) >= 60:
                                close = sdf['close'].values
                                
                                momentum_20d = (close[-1] / close[-20] - 1) * 100
                                momentum_60d = (close[-1] / close[0] - 1) * 100
                                price_to_ma20 = (close[-1] / np.mean(close[-20:]) - 1) * 100
                                
                                # 简化打分
                                score = 50 + momentum_20d * 0.5 + momentum_60d * 0.3
                                if price_to_ma20 > 0:
                                    score += 10
                                
                                if score >= self.swing_engine.min_score:
                                    scores[stock] = score
                        except:
                            continue
                
                candidates = [
                    {'symbol': s, 'total_score': sc, 'stage': 'S2', 'name': ''}
                    for s, sc in sorted(scores.items(), key=lambda x: x[1], reverse=True)
                ]
                
                # 生成交易信号
                signals = self.swing_engine.generate_signals(candidates, positions)
                
                # 执行交易
                for signal in signals:
                    stock = signal['symbol']
                    
                    if signal['action'] == 'SELL' and stock in positions:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            value = positions[stock]['shares'] * price * 0.9985  # 扣费
                            cash += value
                            trades.append({
                                'date': date,
                                'symbol': stock,
                                'action': 'SELL',
                                'price': price,
                                'shares': positions[stock]['shares'],
                                'reason': signal['reason']
                            })
                            del positions[stock]
                    
                    elif signal['action'] == 'BUY' and stock not in positions:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            target_value = portfolio_value / self.swing_engine.max_holdings
                            buy_value = min(target_value, cash)
                            shares = int(buy_value / price / 100) * 100
                            
                            if shares > 0:
                                cost = shares * price * 1.0003  # 扣费
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {
                                        'shares': shares,
                                        'cost': price,
                                        'highest_price': price,
                                        'current_price': price
                                    }
                                    trades.append({
                                        'date': date,
                                        'symbol': stock,
                                        'action': 'BUY',
                                        'price': price,
                                        'shares': shares,
                                        'reason': signal['reason']
                                    })
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
            
            equity_curve.append(portfolio_value)
        
        # 计算指标
        equity = pd.Series(equity_curve)
        returns = equity.pct_change().fillna(0)
        
        total_return = (equity.iloc[-1] / initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        calmar = annual_return / max_dd if max_dd > 0 else 0
        
        logger.info(f"✅ 回测完成")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化收益: {annual_return*100:.2f}%")
        logger.info(f"   夏普比率: {sharpe:.2f}")
        logger.info(f"   最大回撤: {max_dd*100:.2f}%")
        
        return {
            'success': True,
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'calmar_ratio': calmar,
                'max_drawdown': max_dd,
                'volatility': volatility
            },
            'equity_curve': equity_curve,
            'trades': trades,
            'trade_count': len(trades)
        }
    
    def generate_report(self, scan_results: List[Dict], backtest_results: Dict) -> str:
        """生成HTML报告"""
        metrics = backtest_results.get('metrics', {})
        top_candidates = self.get_top_candidates(scan_results, 5)
        
        # 生成图表
        chart_html = ""
        if MATPLOTLIB_AVAILABLE and backtest_results.get('equity_curve'):
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            equity = backtest_results['equity_curve']
            axes[0].plot(equity, linewidth=2, color='#667eea')
            axes[0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#667eea')
            axes[0].set_title('Portfolio Value', fontweight='bold')
            axes[0].grid(True, alpha=0.3)
            
            # 回撤
            equity_s = pd.Series(equity)
            peak = equity_s.cummax()
            dd = (equity_s - peak) / peak
            axes[1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
            axes[1].set_title('Drawdown (%)', fontweight='bold')
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            chart_b64 = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股多因子量化系统报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; padding: 30px; margin: 0; min-height: 100vh; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; box-shadow: 0 20px 60px rgba(102,126,234,0.3); }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }}
        .header p {{ margin: 8px 0; opacity: 0.9; font-size: 1.1em; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }}
        .metric .value {{ font-size: 2.5em; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .metric .value.positive {{ background: linear-gradient(135deg, #4ade80, #22c55e); -webkit-background-clip: text; }}
        .metric .value.negative {{ background: linear-gradient(135deg, #f87171, #ef4444); -webkit-background-clip: text; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; backdrop-filter: blur(10px); }}
        .section h2 {{ color: #667eea; margin-top: 0; font-size: 1.6em; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 15px; }}
        .chart {{ text-align: center; margin: 25px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); font-weight: 600; }}
        tr:hover {{ background: rgba(102,126,234,0.1); }}
        .tag {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 0.85em; margin: 3px; }}
        .tag-s {{ background: linear-gradient(135deg, #4ade80, #22c55e); color: white; }}
        .tag-a {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
        .tag-stage {{ background: rgba(251,191,36,0.2); color: #fbbf24; }}
        .highlight {{ color: #4ade80; font-weight: bold; }}
        .stock-card {{ background: rgba(255,255,255,0.05); border-radius: 16px; padding: 25px; margin: 15px 0; border-left: 4px solid #667eea; }}
        .stock-card h3 {{ margin: 0 0 15px 0; color: #667eea; }}
        .signals {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股多因子量化系统</h1>
            <p>整合阶段识别 | 7维评分卡 | 多因子打分 | 科技主线聚焦</p>
            <p>目标：聚焦5只以内股票，波段操作，控制回撤</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">交易次数</div>
                <div class="value">{backtest_results.get('trade_count', 0)}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        <div class="section">
            <h2>🎯 Top 5 候选股票</h2>
            {''.join([f'''
            <div class="stock-card">
                <h3>{c.get('name', '')} ({c.get('symbol', '')})</h3>
                <p><span class="tag tag-{'s' if c.get('scorecard_grade','C') in ['S+','S'] else 'a'}">评分: {c.get('total_score', 0):.1f}</span>
                   <span class="tag tag-stage">阶段: {c.get('stage', 'S0')}</span>
                   <span class="tag">推荐: {c.get('recommendation', '')}</span></p>
                <div class="signals">
                    {''.join([f'<span class="tag" style="background:rgba(74,222,128,0.2);color:#4ade80">{s}</span>' for s in c.get('stage_signals', [])[:3]])}
                    {''.join([f'<span class="tag" style="background:rgba(102,126,234,0.2);color:#667eea">{s}</span>' for s in c.get('scorecard_signals', [])[:3]])}
                </div>
            </div>
            ''' for c in top_candidates])}
        </div>
        
        <div class="section">
            <h2>📋 系统说明</h2>
            <table>
                <tr><th>模块</th><th>说明</th></tr>
                <tr><td>阶段识别</td><td>S0(观察)→S1(验证)→S2(导入,最佳买点)→S3(放量)→S4(加速)→S5(成熟)</td></tr>
                <tr><td>7维评分卡</td><td>盈利能力/成长性/财务健康/估值水平/行业地位/管理质量/市场表现</td></tr>
                <tr><td>多因子打分</td><td>基本面(40%)+估值(15%)+技术(25%)+阶段(20%)</td></tr>
                <tr><td>科技主线</td><td>AI/半导体/新能源/量子计算/生物医药</td></tr>
                <tr><td>波段操作</td><td>止损{self.swing_engine.stop_loss*100:.0f}%/止盈{self.swing_engine.take_profit*100:.0f}%/移动止损{self.swing_engine.trailing_stop*100:.0f}%</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
        
        return html


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股多因子量化系统")
    logger.info("=" * 80)
    
    # 配置
    config = {
        'jqdata_username': '13327806797',
        'max_holdings': 5,
        'stop_loss': -0.10,
        'take_profit': 0.50,
        'trailing_stop': 0.15,
        'min_score': 65,
        'rebalance_days': 10,
    }
    
    # 创建系统
    system = TenbaggerMultifactorSystem(config)
    
    # 1. 扫描并打分
    scan_date = datetime.now().strftime('%Y-%m-%d')
    scan_results = system.scan_and_score(scan_date)
    
    # 2. 回测
    backtest_results = system.run_backtest(
        start_date="2024-01-01",
        end_date="2025-12-20",
        initial_capital=1000000
    )
    
    # 3. 生成报告
    logger.info("📝 生成报告...")
    html = system.generate_report(scan_results, backtest_results)
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_multifactor_system_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告已保存: {report_path}")
    
    # 登出
    jq.logout()
    
    # 打印Top候选
    logger.info("\n🎯 Top 5 候选股票:")
    for c in system.get_top_candidates(scan_results, 5):
        logger.info(f"   {c['name']} ({c['symbol']}): 得分 {c['total_score']:.1f}, 阶段 {c['stage']}")
    
    logger.info("=" * 80)
    
    return {
        'scan_results': scan_results,
        'backtest_results': backtest_results,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
十倍股多因子量化系统 - 早期识别与波段操作
==========================================

整合知识库核心逻辑：
1. 阶段识别系统（S0-S5）
2. 7维评分卡
3. 多因子打分模型
4. 科技主线识别
5. 波段操作+回撤控制

目标：聚焦5只以内股票，获取10倍以上回报

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_multifactor_system.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 阶段定义
# ============================================================

class Stage(Enum):
    """十倍股成长阶段"""
    S0 = "S0"  # 观察期 - 有产业链位置，无明显兑现信号
    S1 = "S1"  # 验证期 - 送样/认证中，尚未确认客户
    S2 = "S2"  # 导入期 - 已进入客户体系，最佳介入点
    S3 = "S3"  # 放量期 - 批量订单，扩产明确
    S4 = "S4"  # 加速期 - 业绩拐点，估值修复
    S5 = "S5"  # 成熟期 - 主流共识，十倍股特征消失


STAGE_WEIGHTS = {
    Stage.S0: 0.2,
    Stage.S1: 0.5,
    Stage.S2: 1.0,  # 最佳介入
    Stage.S3: 0.8,
    Stage.S4: 0.4,
    Stage.S5: 0.1,
}


# ============================================================
# 科技主线板块
# ============================================================

TECH_MAINLINE_INDUSTRIES = {
    # AI人工智能
    "AI芯片": ["算力", "GPU", "NPU", "ASIC"],
    "AI算法": ["大模型", "机器学习", "深度学习"],
    "AI应用": ["智能驾驶", "机器人", "具身智能"],
    
    # 半导体
    "半导体设备": ["光刻", "刻蚀", "薄膜沉积", "离子注入"],
    "半导体材料": ["光刻胶", "特种气体", "靶材", "CMP"],
    "芯片设计": ["CPU", "GPU", "存储芯片", "MCU"],
    
    # 新能源
    "锂电池": ["正极材料", "负极材料", "隔膜", "电解液"],
    "光伏": ["硅料", "硅片", "电池片", "组件"],
    "储能": ["储能系统", "逆变器", "BMS"],
    
    # 其他高科技
    "量子计算": ["量子芯片", "量子通信"],
    "生物医药": ["创新药", "CXO", "医疗器械"],
}

TECH_KEYWORDS = [
    "AI", "人工智能", "大模型", "算力", "芯片", "半导体", "GPU", "CPU",
    "机器人", "自动驾驶", "智能驾驶", "新能源", "锂电", "光伏", "储能",
    "量子", "生物医药", "创新药", "5G", "6G", "物联网", "边缘计算"
]


# ============================================================
# 7维评分卡
# ============================================================

@dataclass
class ScorecardResult:
    """评分卡结果"""
    symbol: str
    name: str
    total_score: float
    grade: str
    dimensions: Dict[str, float]
    signals: List[str]


class ScoreCardEngine:
    """7维评分卡引擎"""
    
    # 维度权重
    DIMENSION_WEIGHTS = {
        "profitability": 0.15,      # 盈利能力
        "growth": 0.20,             # 成长性
        "financial_health": 0.10,   # 财务健康
        "valuation": 0.15,          # 估值水平
        "industry_position": 0.15,  # 行业地位
        "management": 0.10,         # 管理质量
        "market_performance": 0.15, # 市场表现
    }
    
    def compute(self, symbol: str, name: str, data: Dict) -> ScorecardResult:
        """计算评分"""
        scores = {}
        signals = []
        
        # 1. 盈利能力
        roe = data.get('roe', 0)
        gross_margin = data.get('gross_margin', 0)
        
        profitability_score = 0
        if roe > 20:
            profitability_score = 100
            signals.append(f"ROE极高({roe:.1f}%)")
        elif roe > 15:
            profitability_score = 80
        elif roe > 10:
            profitability_score = 60
        elif roe > 5:
            profitability_score = 40
        else:
            profitability_score = 20
        
        if gross_margin > 40:
            profitability_score = min(100, profitability_score + 20)
            signals.append(f"毛利率高({gross_margin:.1f}%)")
        
        scores['profitability'] = profitability_score
        
        # 2. 成长性
        revenue_growth = data.get('revenue_growth', 0)
        profit_growth = data.get('profit_growth', 0)
        
        growth_score = 0
        if revenue_growth > 50:
            growth_score = 100
            signals.append(f"营收高增长({revenue_growth:.0f}%)")
        elif revenue_growth > 30:
            growth_score = 80
        elif revenue_growth > 15:
            growth_score = 60
        elif revenue_growth > 0:
            growth_score = 40
        else:
            growth_score = 20
        
        if profit_growth > 50:
            growth_score = min(100, growth_score + 20)
            signals.append(f"利润高增长({profit_growth:.0f}%)")
        
        scores['growth'] = growth_score
        
        # 3. 财务健康
        debt_ratio = data.get('debt_ratio', 50)
        current_ratio = data.get('current_ratio', 1)
        
        health_score = 0
        if debt_ratio < 30:
            health_score = 100
        elif debt_ratio < 50:
            health_score = 80
        elif debt_ratio < 70:
            health_score = 60
        else:
            health_score = 40
        
        if current_ratio > 2:
            health_score = min(100, health_score + 10)
        
        scores['financial_health'] = health_score
        
        # 4. 估值水平
        pe = data.get('pe', 50)
        pb = data.get('pb', 3)
        
        valuation_score = 0
        if 0 < pe < 20:
            valuation_score = 100
            signals.append(f"估值合理(PE={pe:.0f})")
        elif 20 <= pe < 40:
            valuation_score = 70
        elif 40 <= pe < 80:
            valuation_score = 50
        else:
            valuation_score = 30
        
        scores['valuation'] = valuation_score
        
        # 5. 行业地位
        market_share = data.get('market_share', 0)
        is_leader = data.get('is_leader', False)
        
        industry_score = 50  # 默认中等
        if is_leader:
            industry_score = 90
            signals.append("行业龙头")
        elif market_share > 10:
            industry_score = 70
        
        scores['industry_position'] = industry_score
        
        # 6. 管理质量
        rd_ratio = data.get('rd_ratio', 0)  # 研发投入占比
        
        management_score = 50
        if rd_ratio > 10:
            management_score = 90
            signals.append(f"研发投入高({rd_ratio:.1f}%)")
        elif rd_ratio > 5:
            management_score = 70
        
        scores['management'] = management_score
        
        # 7. 市场表现
        momentum_20d = data.get('momentum_20d', 0)
        momentum_60d = data.get('momentum_60d', 0)
        vol_ratio = data.get('vol_ratio', 1)
        
        market_score = 50
        if momentum_20d > 20 and momentum_60d > 30:
            market_score = 90
            signals.append("强势动量")
        elif momentum_20d > 10:
            market_score = 70
        elif momentum_20d < -10:
            market_score = 30
        
        if vol_ratio > 2:
            market_score = min(100, market_score + 10)
            signals.append("放量突破")
        
        scores['market_performance'] = market_score
        
        # 计算总分
        total_score = sum(scores[k] * self.DIMENSION_WEIGHTS[k] for k in scores)
        
        # 确定等级
        if total_score >= 85:
            grade = "S+"
        elif total_score >= 75:
            grade = "S"
        elif total_score >= 65:
            grade = "A"
        elif total_score >= 50:
            grade = "B"
        elif total_score >= 35:
            grade = "C"
        else:
            grade = "D"
        
        return ScorecardResult(
            symbol=symbol,
            name=name,
            total_score=total_score,
            grade=grade,
            dimensions=scores,
            signals=signals
        )


# ============================================================
# 阶段识别引擎
# ============================================================

class StageIdentifier:
    """阶段识别引擎"""
    
    def identify(self, data: Dict) -> Tuple[Stage, float, List[str]]:
        """
        识别股票所处阶段
        
        Returns:
            (阶段, 置信度, 信号列表)
        """
        signals = []
        
        revenue_growth = data.get('revenue_growth', 0)
        profit_growth = data.get('profit_growth', 0)
        momentum_20d = data.get('momentum_20d', 0)
        momentum_60d = data.get('momentum_60d', 0)
        vol_ratio = data.get('vol_ratio', 1)
        pe = data.get('pe', 50)
        market_cap = data.get('market_cap', 100)  # 亿
        
        # S4加速期: 业绩爆发，估值修复
        if revenue_growth > 80 and profit_growth > 100 and momentum_60d > 50:
            signals.append("业绩拐点确认")
            signals.append("估值快速修复")
            return Stage.S4, 0.85, signals
        
        # S3放量期: 批量订单，扩产
        if revenue_growth > 50 and profit_growth > 60 and vol_ratio > 1.5:
            signals.append("营收高速增长")
            signals.append("放量上涨")
            if momentum_20d > 15:
                return Stage.S3, 0.80, signals
        
        # S2导入期 (最佳买点): 小批量验证通过
        if 30 <= revenue_growth <= 60 and 20 <= profit_growth <= 60:
            if momentum_20d > 5 and market_cap < 300:
                signals.append("成长黄金期")
                signals.append("市值适中")
                return Stage.S2, 0.75, signals
        
        # S1验证期: 有增长但未放量
        if 15 <= revenue_growth < 40 and profit_growth > 10:
            signals.append("增长验证中")
            return Stage.S1, 0.60, signals
        
        # S5成熟期: 大市值，低增速
        if market_cap > 1000 and revenue_growth < 15:
            signals.append("增长放缓")
            return Stage.S5, 0.70, signals
        
        # S0观察期
        signals.append("待进一步验证")
        return Stage.S0, 0.40, signals


# ============================================================
# 多因子打分系统
# ============================================================

class MultifactorScorer:
    """多因子打分系统"""
    
    # 因子权重
    FACTOR_WEIGHTS = {
        # 基本面因子 (40%)
        'roe': 0.08,
        'revenue_growth': 0.10,
        'profit_growth': 0.08,
        'gross_margin': 0.06,
        'rd_ratio': 0.08,
        
        # 估值因子 (15%)
        'pe_score': 0.08,
        'pb_score': 0.07,
        
        # 技术因子 (25%)
        'momentum_20d': 0.10,
        'momentum_60d': 0.08,
        'vol_ratio': 0.07,
        
        # 阶段因子 (20%)
        'stage_score': 0.20,
    }
    
    def __init__(self):
        self.stage_identifier = StageIdentifier()
        self.scorecard_engine = ScoreCardEngine()
    
    def score(self, symbol: str, name: str, data: Dict) -> Dict:
        """计算综合得分"""
        
        # 1. 阶段识别
        stage, stage_confidence, stage_signals = self.stage_identifier.identify(data)
        stage_score = STAGE_WEIGHTS.get(stage, 0.2) * 100
        
        # 2. 评分卡
        scorecard = self.scorecard_engine.compute(symbol, name, data)
        
        # 3. 因子得分
        factor_scores = {}
        
        # 基本面因子
        factor_scores['roe'] = min(100, max(0, data.get('roe', 0) * 5))
        factor_scores['revenue_growth'] = min(100, max(0, data.get('revenue_growth', 0) * 2))
        factor_scores['profit_growth'] = min(100, max(0, data.get('profit_growth', 0) * 1.5))
        factor_scores['gross_margin'] = min(100, max(0, data.get('gross_margin', 0) * 2))
        factor_scores['rd_ratio'] = min(100, max(0, data.get('rd_ratio', 0) * 10))
        
        # 估值因子 (低PE/PB得高分)
        pe = data.get('pe', 50)
        factor_scores['pe_score'] = max(0, 100 - pe * 1.5) if pe > 0 else 50
        
        pb = data.get('pb', 3)
        factor_scores['pb_score'] = max(0, 100 - pb * 20) if pb > 0 else 50
        
        # 技术因子
        factor_scores['momentum_20d'] = min(100, max(0, 50 + data.get('momentum_20d', 0) * 2))
        factor_scores['momentum_60d'] = min(100, max(0, 50 + data.get('momentum_60d', 0)))
        factor_scores['vol_ratio'] = min(100, max(0, data.get('vol_ratio', 1) * 40))
        
        # 阶段因子
        factor_scores['stage_score'] = stage_score
        
        # 4. 计算加权总分
        total_score = sum(
            factor_scores.get(k, 50) * self.FACTOR_WEIGHTS[k]
            for k in self.FACTOR_WEIGHTS
        )
        
        # 5. 科技主线加成
        tech_bonus = 0
        industry = data.get('industry', '')
        for keyword in TECH_KEYWORDS:
            if keyword in industry or keyword in name:
                tech_bonus = 10
                break
        
        total_score = min(100, total_score + tech_bonus)
        
        return {
            'symbol': symbol,
            'name': name,
            'total_score': round(total_score, 1),
            'stage': stage.value,
            'stage_confidence': stage_confidence,
            'stage_signals': stage_signals,
            'scorecard_grade': scorecard.grade,
            'scorecard_score': scorecard.total_score,
            'scorecard_signals': scorecard.signals,
            'factor_scores': factor_scores,
            'tech_bonus': tech_bonus,
            'recommendation': self._get_recommendation(total_score, stage)
        }
    
    def _get_recommendation(self, score: float, stage: Stage) -> str:
        """生成推荐"""
        if score >= 80 and stage in [Stage.S1, Stage.S2]:
            return "强烈推荐 - 早期布局良机"
        elif score >= 70 and stage in [Stage.S2, Stage.S3]:
            return "推荐 - 成长黄金期"
        elif score >= 60:
            return "关注 - 等待更好时机"
        elif score >= 50:
            return "观察 - 需更多验证"
        else:
            return "不推荐"


# ============================================================
# 波段操作引擎
# ============================================================

class SwingTradeEngine:
    """波段操作引擎"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.max_holdings = self.config.get('max_holdings', 5)
        self.stop_loss = self.config.get('stop_loss', -0.10)
        self.take_profit = self.config.get('take_profit', 0.50)
        self.trailing_stop = self.config.get('trailing_stop', 0.15)
        self.min_score = self.config.get('min_score', 70)
    
    def generate_signals(self, candidates: List[Dict], current_positions: Dict) -> List[Dict]:
        """
        生成交易信号
        
        Args:
            candidates: 候选股票列表 (已按得分排序)
            current_positions: 当前持仓 {symbol: {shares, cost, highest_price}}
        
        Returns:
            交易信号列表
        """
        signals = []
        
        # 1. 检查卖出信号
        for symbol, pos in current_positions.items():
            cost = pos['cost']
            current_price = pos.get('current_price', cost)
            highest_price = pos.get('highest_price', current_price)
            
            pnl = (current_price - cost) / cost
            drawdown_from_high = (current_price - highest_price) / highest_price if highest_price > 0 else 0
            
            # 止损
            if pnl <= self.stop_loss:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'止损 ({pnl*100:.1f}%)',
                    'priority': 1
                })
                continue
            
            # 止盈
            if pnl >= self.take_profit:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'止盈 ({pnl*100:.1f}%)',
                    'priority': 2
                })
                continue
            
            # 移动止损
            if drawdown_from_high <= -self.trailing_stop:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'移动止损 (从高点回撤 {drawdown_from_high*100:.1f}%)',
                    'priority': 3
                })
        
        # 2. 检查买入信号
        current_count = len(current_positions) - sum(1 for s in signals if s['action'] == 'SELL')
        slots_available = self.max_holdings - current_count
        
        if slots_available > 0:
            for candidate in candidates:
                if len([s for s in signals if s['action'] == 'BUY']) >= slots_available:
                    break
                
                symbol = candidate['symbol']
                
                # 跳过已持有
                if symbol in current_positions:
                    continue
                
                # 检查得分
                if candidate['total_score'] < self.min_score:
                    continue
                
                # 只在S1-S3阶段买入
                stage = candidate.get('stage', 'S0')
                if stage not in ['S1', 'S2', 'S3']:
                    continue
                
                signals.append({
                    'symbol': symbol,
                    'name': candidate.get('name', ''),
                    'action': 'BUY',
                    'reason': f"得分 {candidate['total_score']:.1f}, 阶段 {stage}",
                    'score': candidate['total_score'],
                    'stage': stage,
                    'priority': 10 - int(candidate['total_score'] / 10)  # 高分优先
                })
        
        # 按优先级排序
        signals.sort(key=lambda x: x['priority'])
        
        return signals


# ============================================================
# 主系统
# ============================================================

class TenbaggerMultifactorSystem:
    """十倍股多因子量化系统"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.jqdata_username = self.config.get('jqdata_username', '13327806797')
        self.scorer = MultifactorScorer()
        self.swing_engine = SwingTradeEngine(self.config)
        self.jq_authenticated = False
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth(self.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def get_tech_universe(self) -> List[str]:
        """获取科技主线股票池"""
        # 中证科技100 + 创业板指成分股
        stocks = []
        
        try:
            # 创业板
            stocks += jq.get_index_stocks('399006.XSHE')[:50]
            # 科创50
            stocks += jq.get_index_stocks('000688.XSHG')[:30] if jq.get_index_stocks('000688.XSHG') else []
            # 中证500中的科技股 (通过行业筛选)
            zz500 = jq.get_index_stocks('000905.XSHG')
            
            # 筛选科技行业
            for stock in zz500[:100]:
                try:
                    info = jq.get_security_info(stock)
                    if info and any(kw in info.display_name for kw in TECH_KEYWORDS):
                        stocks.append(stock)
                except:
                    continue
        except:
            pass
        
        return list(set(stocks))
    
    def fetch_stock_data(self, stock: str, date: str) -> Dict:
        """获取股票数据"""
        data = {'symbol': stock}
        
        try:
            # 基本信息
            info = jq.get_security_info(stock)
            if info:
                data['name'] = info.display_name
            
            # 基本面数据
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.market_cap,
                jq.indicator.roe,
                jq.indicator.roa,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin
            ).filter(jq.valuation.code == stock)
            
            fund_df = jq.get_fundamentals(q, date=date)
            
            if not fund_df.empty:
                data['pe'] = fund_df['pe_ratio'].iloc[0] or 50
                data['pb'] = fund_df['pb_ratio'].iloc[0] or 3
                data['market_cap'] = (fund_df['market_cap'].iloc[0] or 100) / 100000000  # 转亿
                data['roe'] = fund_df['roe'].iloc[0] or 0
                data['roa'] = fund_df['roa'].iloc[0] or 0
                data['revenue_growth'] = fund_df['inc_revenue_year_on_year'].iloc[0] or 0
                data['profit_growth'] = fund_df['inc_net_profit_year_on_year'].iloc[0] or 0
                data['gross_margin'] = fund_df['gross_profit_margin'].iloc[0] or 0
            
            # 技术数据
            price_df = jq.get_price(
                stock, end_date=date, count=60,
                frequency='daily', fields=['close', 'volume']
            )
            
            if price_df is not None and len(price_df) >= 60:
                close = price_df['close'].values
                volume = price_df['volume'].values
                
                data['momentum_5d'] = (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0
                data['momentum_20d'] = (close[-1] / close[-20] - 1) * 100 if close[-20] > 0 else 0
                data['momentum_60d'] = (close[-1] / close[0] - 1) * 100 if close[0] > 0 else 0
                data['vol_ratio'] = np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1
                data['current_price'] = close[-1]
            
            # 行业
            try:
                ind = jq.get_industry(stock, date=date)
                if ind and stock in ind:
                    data['industry'] = ind[stock].get('sw_l1', {}).get('industry_name', '')
            except:
                data['industry'] = ''
            
        except Exception as e:
            logger.warning(f"获取{stock}数据失败: {e}")
        
        return data
    
    def scan_and_score(self, date: str = None) -> List[Dict]:
        """扫描并打分"""
        if not self.authenticate_jqdata():
            return []
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📊 开始扫描 ({date})...")
        
        # 获取股票池
        universe = self.get_tech_universe()
        logger.info(f"   股票池: {len(universe)}只")
        
        # 扫描并打分
        results = []
        for i, stock in enumerate(universe):
            if i % 20 == 0:
                logger.info(f"   进度: {i}/{len(universe)}")
            
            data = self.fetch_stock_data(stock, date)
            if data.get('name'):
                score_result = self.scorer.score(stock, data.get('name', ''), data)
                score_result['data'] = data
                results.append(score_result)
        
        # 按得分排序
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        logger.info(f"✅ 扫描完成: {len(results)}只股票")
        
        return results
    
    def get_top_candidates(self, results: List[Dict], top_n: int = 5) -> List[Dict]:
        """获取Top候选"""
        # 只保留S1-S3阶段的高分股票
        filtered = [
            r for r in results
            if r['total_score'] >= 70 and r.get('stage', 'S0') in ['S1', 'S2', 'S3']
        ]
        
        return filtered[:top_n]
    
    def run_backtest(self, start_date: str, end_date: str, initial_capital: float = 1000000) -> Dict:
        """运行回测"""
        if not self.authenticate_jqdata():
            return {'success': False, 'error': 'JQData认证失败'}
        
        logger.info(f"🚀 开始回测: {start_date} ~ {end_date}")
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [str(d) for d in trade_days]
        
        # 获取股票池
        universe = self.get_tech_universe()[:50]  # 限制数量
        
        # 预加载价格数据
        logger.info("   预加载价格数据...")
        price_df = jq.get_price(
            universe,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None:
            for stock in universe:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        # 初始化
        cash = initial_capital
        positions = {}
        equity_curve = [cash]
        trades = []
        
        rebalance_days = self.config.get('rebalance_days', 10)
        counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
            
            # 更新持仓价值和最高价
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    current_price = price_cache[stock].loc[date, 'close']
                    pos['current_price'] = current_price
                    pos['highest_price'] = max(pos.get('highest_price', current_price), current_price)
                    portfolio_value += pos['shares'] * current_price
            
            # 调仓检查
            counter += 1
            if counter >= rebalance_days:
                counter = 0
                
                # 简化版: 基于动量和价格位置打分
                scores = {}
                for stock in universe:
                    if stock in price_cache:
                        try:
                            sdf = price_cache[stock]
                            mask = sdf.index <= date
                            sdf = sdf[mask].tail(60)
                            
                            if len(sdf) >= 60:
                                close = sdf['close'].values
                                
                                momentum_20d = (close[-1] / close[-20] - 1) * 100
                                momentum_60d = (close[-1] / close[0] - 1) * 100
                                price_to_ma20 = (close[-1] / np.mean(close[-20:]) - 1) * 100
                                
                                # 简化打分
                                score = 50 + momentum_20d * 0.5 + momentum_60d * 0.3
                                if price_to_ma20 > 0:
                                    score += 10
                                
                                if score >= self.swing_engine.min_score:
                                    scores[stock] = score
                        except:
                            continue
                
                candidates = [
                    {'symbol': s, 'total_score': sc, 'stage': 'S2', 'name': ''}
                    for s, sc in sorted(scores.items(), key=lambda x: x[1], reverse=True)
                ]
                
                # 生成交易信号
                signals = self.swing_engine.generate_signals(candidates, positions)
                
                # 执行交易
                for signal in signals:
                    stock = signal['symbol']
                    
                    if signal['action'] == 'SELL' and stock in positions:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            value = positions[stock]['shares'] * price * 0.9985  # 扣费
                            cash += value
                            trades.append({
                                'date': date,
                                'symbol': stock,
                                'action': 'SELL',
                                'price': price,
                                'shares': positions[stock]['shares'],
                                'reason': signal['reason']
                            })
                            del positions[stock]
                    
                    elif signal['action'] == 'BUY' and stock not in positions:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            target_value = portfolio_value / self.swing_engine.max_holdings
                            buy_value = min(target_value, cash)
                            shares = int(buy_value / price / 100) * 100
                            
                            if shares > 0:
                                cost = shares * price * 1.0003  # 扣费
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {
                                        'shares': shares,
                                        'cost': price,
                                        'highest_price': price,
                                        'current_price': price
                                    }
                                    trades.append({
                                        'date': date,
                                        'symbol': stock,
                                        'action': 'BUY',
                                        'price': price,
                                        'shares': shares,
                                        'reason': signal['reason']
                                    })
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
            
            equity_curve.append(portfolio_value)
        
        # 计算指标
        equity = pd.Series(equity_curve)
        returns = equity.pct_change().fillna(0)
        
        total_return = (equity.iloc[-1] / initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        calmar = annual_return / max_dd if max_dd > 0 else 0
        
        logger.info(f"✅ 回测完成")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化收益: {annual_return*100:.2f}%")
        logger.info(f"   夏普比率: {sharpe:.2f}")
        logger.info(f"   最大回撤: {max_dd*100:.2f}%")
        
        return {
            'success': True,
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'calmar_ratio': calmar,
                'max_drawdown': max_dd,
                'volatility': volatility
            },
            'equity_curve': equity_curve,
            'trades': trades,
            'trade_count': len(trades)
        }
    
    def generate_report(self, scan_results: List[Dict], backtest_results: Dict) -> str:
        """生成HTML报告"""
        metrics = backtest_results.get('metrics', {})
        top_candidates = self.get_top_candidates(scan_results, 5)
        
        # 生成图表
        chart_html = ""
        if MATPLOTLIB_AVAILABLE and backtest_results.get('equity_curve'):
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            equity = backtest_results['equity_curve']
            axes[0].plot(equity, linewidth=2, color='#667eea')
            axes[0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#667eea')
            axes[0].set_title('Portfolio Value', fontweight='bold')
            axes[0].grid(True, alpha=0.3)
            
            # 回撤
            equity_s = pd.Series(equity)
            peak = equity_s.cummax()
            dd = (equity_s - peak) / peak
            axes[1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
            axes[1].set_title('Drawdown (%)', fontweight='bold')
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            chart_b64 = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股多因子量化系统报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; padding: 30px; margin: 0; min-height: 100vh; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; box-shadow: 0 20px 60px rgba(102,126,234,0.3); }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }}
        .header p {{ margin: 8px 0; opacity: 0.9; font-size: 1.1em; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }}
        .metric .value {{ font-size: 2.5em; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .metric .value.positive {{ background: linear-gradient(135deg, #4ade80, #22c55e); -webkit-background-clip: text; }}
        .metric .value.negative {{ background: linear-gradient(135deg, #f87171, #ef4444); -webkit-background-clip: text; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; backdrop-filter: blur(10px); }}
        .section h2 {{ color: #667eea; margin-top: 0; font-size: 1.6em; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 15px; }}
        .chart {{ text-align: center; margin: 25px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); font-weight: 600; }}
        tr:hover {{ background: rgba(102,126,234,0.1); }}
        .tag {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 0.85em; margin: 3px; }}
        .tag-s {{ background: linear-gradient(135deg, #4ade80, #22c55e); color: white; }}
        .tag-a {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
        .tag-stage {{ background: rgba(251,191,36,0.2); color: #fbbf24; }}
        .highlight {{ color: #4ade80; font-weight: bold; }}
        .stock-card {{ background: rgba(255,255,255,0.05); border-radius: 16px; padding: 25px; margin: 15px 0; border-left: 4px solid #667eea; }}
        .stock-card h3 {{ margin: 0 0 15px 0; color: #667eea; }}
        .signals {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股多因子量化系统</h1>
            <p>整合阶段识别 | 7维评分卡 | 多因子打分 | 科技主线聚焦</p>
            <p>目标：聚焦5只以内股票，波段操作，控制回撤</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">交易次数</div>
                <div class="value">{backtest_results.get('trade_count', 0)}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        <div class="section">
            <h2>🎯 Top 5 候选股票</h2>
            {''.join([f'''
            <div class="stock-card">
                <h3>{c.get('name', '')} ({c.get('symbol', '')})</h3>
                <p><span class="tag tag-{'s' if c.get('scorecard_grade','C') in ['S+','S'] else 'a'}">评分: {c.get('total_score', 0):.1f}</span>
                   <span class="tag tag-stage">阶段: {c.get('stage', 'S0')}</span>
                   <span class="tag">推荐: {c.get('recommendation', '')}</span></p>
                <div class="signals">
                    {''.join([f'<span class="tag" style="background:rgba(74,222,128,0.2);color:#4ade80">{s}</span>' for s in c.get('stage_signals', [])[:3]])}
                    {''.join([f'<span class="tag" style="background:rgba(102,126,234,0.2);color:#667eea">{s}</span>' for s in c.get('scorecard_signals', [])[:3]])}
                </div>
            </div>
            ''' for c in top_candidates])}
        </div>
        
        <div class="section">
            <h2>📋 系统说明</h2>
            <table>
                <tr><th>模块</th><th>说明</th></tr>
                <tr><td>阶段识别</td><td>S0(观察)→S1(验证)→S2(导入,最佳买点)→S3(放量)→S4(加速)→S5(成熟)</td></tr>
                <tr><td>7维评分卡</td><td>盈利能力/成长性/财务健康/估值水平/行业地位/管理质量/市场表现</td></tr>
                <tr><td>多因子打分</td><td>基本面(40%)+估值(15%)+技术(25%)+阶段(20%)</td></tr>
                <tr><td>科技主线</td><td>AI/半导体/新能源/量子计算/生物医药</td></tr>
                <tr><td>波段操作</td><td>止损{self.swing_engine.stop_loss*100:.0f}%/止盈{self.swing_engine.take_profit*100:.0f}%/移动止损{self.swing_engine.trailing_stop*100:.0f}%</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
        
        return html


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股多因子量化系统")
    logger.info("=" * 80)
    
    # 配置
    config = {
        'jqdata_username': '13327806797',
        'max_holdings': 5,
        'stop_loss': -0.10,
        'take_profit': 0.50,
        'trailing_stop': 0.15,
        'min_score': 65,
        'rebalance_days': 10,
    }
    
    # 创建系统
    system = TenbaggerMultifactorSystem(config)
    
    # 1. 扫描并打分
    scan_date = datetime.now().strftime('%Y-%m-%d')
    scan_results = system.scan_and_score(scan_date)
    
    # 2. 回测
    backtest_results = system.run_backtest(
        start_date="2024-01-01",
        end_date="2025-12-20",
        initial_capital=1000000
    )
    
    # 3. 生成报告
    logger.info("📝 生成报告...")
    html = system.generate_report(scan_results, backtest_results)
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_multifactor_system_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告已保存: {report_path}")
    
    # 登出
    jq.logout()
    
    # 打印Top候选
    logger.info("\n🎯 Top 5 候选股票:")
    for c in system.get_top_candidates(scan_results, 5):
        logger.info(f"   {c['name']} ({c['symbol']}): 得分 {c['total_score']:.1f}, 阶段 {c['stage']}")
    
    logger.info("=" * 80)
    
    return {
        'scan_results': scan_results,
        'backtest_results': backtest_results,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()






















# -*- coding: utf-8 -*-
"""
十倍股多因子量化系统 - 早期识别与波段操作
==========================================

整合知识库核心逻辑：
1. 阶段识别系统（S0-S5）
2. 7维评分卡
3. 多因子打分模型
4. 科技主线识别
5. 波段操作+回撤控制

目标：聚焦5只以内股票，获取10倍以上回报

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_multifactor_system.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 阶段定义
# ============================================================

class Stage(Enum):
    """十倍股成长阶段"""
    S0 = "S0"  # 观察期 - 有产业链位置，无明显兑现信号
    S1 = "S1"  # 验证期 - 送样/认证中，尚未确认客户
    S2 = "S2"  # 导入期 - 已进入客户体系，最佳介入点
    S3 = "S3"  # 放量期 - 批量订单，扩产明确
    S4 = "S4"  # 加速期 - 业绩拐点，估值修复
    S5 = "S5"  # 成熟期 - 主流共识，十倍股特征消失


STAGE_WEIGHTS = {
    Stage.S0: 0.2,
    Stage.S1: 0.5,
    Stage.S2: 1.0,  # 最佳介入
    Stage.S3: 0.8,
    Stage.S4: 0.4,
    Stage.S5: 0.1,
}


# ============================================================
# 科技主线板块
# ============================================================

TECH_MAINLINE_INDUSTRIES = {
    # AI人工智能
    "AI芯片": ["算力", "GPU", "NPU", "ASIC"],
    "AI算法": ["大模型", "机器学习", "深度学习"],
    "AI应用": ["智能驾驶", "机器人", "具身智能"],
    
    # 半导体
    "半导体设备": ["光刻", "刻蚀", "薄膜沉积", "离子注入"],
    "半导体材料": ["光刻胶", "特种气体", "靶材", "CMP"],
    "芯片设计": ["CPU", "GPU", "存储芯片", "MCU"],
    
    # 新能源
    "锂电池": ["正极材料", "负极材料", "隔膜", "电解液"],
    "光伏": ["硅料", "硅片", "电池片", "组件"],
    "储能": ["储能系统", "逆变器", "BMS"],
    
    # 其他高科技
    "量子计算": ["量子芯片", "量子通信"],
    "生物医药": ["创新药", "CXO", "医疗器械"],
}

TECH_KEYWORDS = [
    "AI", "人工智能", "大模型", "算力", "芯片", "半导体", "GPU", "CPU",
    "机器人", "自动驾驶", "智能驾驶", "新能源", "锂电", "光伏", "储能",
    "量子", "生物医药", "创新药", "5G", "6G", "物联网", "边缘计算"
]


# ============================================================
# 7维评分卡
# ============================================================

@dataclass
class ScorecardResult:
    """评分卡结果"""
    symbol: str
    name: str
    total_score: float
    grade: str
    dimensions: Dict[str, float]
    signals: List[str]


class ScoreCardEngine:
    """7维评分卡引擎"""
    
    # 维度权重
    DIMENSION_WEIGHTS = {
        "profitability": 0.15,      # 盈利能力
        "growth": 0.20,             # 成长性
        "financial_health": 0.10,   # 财务健康
        "valuation": 0.15,          # 估值水平
        "industry_position": 0.15,  # 行业地位
        "management": 0.10,         # 管理质量
        "market_performance": 0.15, # 市场表现
    }
    
    def compute(self, symbol: str, name: str, data: Dict) -> ScorecardResult:
        """计算评分"""
        scores = {}
        signals = []
        
        # 1. 盈利能力
        roe = data.get('roe', 0)
        gross_margin = data.get('gross_margin', 0)
        
        profitability_score = 0
        if roe > 20:
            profitability_score = 100
            signals.append(f"ROE极高({roe:.1f}%)")
        elif roe > 15:
            profitability_score = 80
        elif roe > 10:
            profitability_score = 60
        elif roe > 5:
            profitability_score = 40
        else:
            profitability_score = 20
        
        if gross_margin > 40:
            profitability_score = min(100, profitability_score + 20)
            signals.append(f"毛利率高({gross_margin:.1f}%)")
        
        scores['profitability'] = profitability_score
        
        # 2. 成长性
        revenue_growth = data.get('revenue_growth', 0)
        profit_growth = data.get('profit_growth', 0)
        
        growth_score = 0
        if revenue_growth > 50:
            growth_score = 100
            signals.append(f"营收高增长({revenue_growth:.0f}%)")
        elif revenue_growth > 30:
            growth_score = 80
        elif revenue_growth > 15:
            growth_score = 60
        elif revenue_growth > 0:
            growth_score = 40
        else:
            growth_score = 20
        
        if profit_growth > 50:
            growth_score = min(100, growth_score + 20)
            signals.append(f"利润高增长({profit_growth:.0f}%)")
        
        scores['growth'] = growth_score
        
        # 3. 财务健康
        debt_ratio = data.get('debt_ratio', 50)
        current_ratio = data.get('current_ratio', 1)
        
        health_score = 0
        if debt_ratio < 30:
            health_score = 100
        elif debt_ratio < 50:
            health_score = 80
        elif debt_ratio < 70:
            health_score = 60
        else:
            health_score = 40
        
        if current_ratio > 2:
            health_score = min(100, health_score + 10)
        
        scores['financial_health'] = health_score
        
        # 4. 估值水平
        pe = data.get('pe', 50)
        pb = data.get('pb', 3)
        
        valuation_score = 0
        if 0 < pe < 20:
            valuation_score = 100
            signals.append(f"估值合理(PE={pe:.0f})")
        elif 20 <= pe < 40:
            valuation_score = 70
        elif 40 <= pe < 80:
            valuation_score = 50
        else:
            valuation_score = 30
        
        scores['valuation'] = valuation_score
        
        # 5. 行业地位
        market_share = data.get('market_share', 0)
        is_leader = data.get('is_leader', False)
        
        industry_score = 50  # 默认中等
        if is_leader:
            industry_score = 90
            signals.append("行业龙头")
        elif market_share > 10:
            industry_score = 70
        
        scores['industry_position'] = industry_score
        
        # 6. 管理质量
        rd_ratio = data.get('rd_ratio', 0)  # 研发投入占比
        
        management_score = 50
        if rd_ratio > 10:
            management_score = 90
            signals.append(f"研发投入高({rd_ratio:.1f}%)")
        elif rd_ratio > 5:
            management_score = 70
        
        scores['management'] = management_score
        
        # 7. 市场表现
        momentum_20d = data.get('momentum_20d', 0)
        momentum_60d = data.get('momentum_60d', 0)
        vol_ratio = data.get('vol_ratio', 1)
        
        market_score = 50
        if momentum_20d > 20 and momentum_60d > 30:
            market_score = 90
            signals.append("强势动量")
        elif momentum_20d > 10:
            market_score = 70
        elif momentum_20d < -10:
            market_score = 30
        
        if vol_ratio > 2:
            market_score = min(100, market_score + 10)
            signals.append("放量突破")
        
        scores['market_performance'] = market_score
        
        # 计算总分
        total_score = sum(scores[k] * self.DIMENSION_WEIGHTS[k] for k in scores)
        
        # 确定等级
        if total_score >= 85:
            grade = "S+"
        elif total_score >= 75:
            grade = "S"
        elif total_score >= 65:
            grade = "A"
        elif total_score >= 50:
            grade = "B"
        elif total_score >= 35:
            grade = "C"
        else:
            grade = "D"
        
        return ScorecardResult(
            symbol=symbol,
            name=name,
            total_score=total_score,
            grade=grade,
            dimensions=scores,
            signals=signals
        )


# ============================================================
# 阶段识别引擎
# ============================================================

class StageIdentifier:
    """阶段识别引擎"""
    
    def identify(self, data: Dict) -> Tuple[Stage, float, List[str]]:
        """
        识别股票所处阶段
        
        Returns:
            (阶段, 置信度, 信号列表)
        """
        signals = []
        
        revenue_growth = data.get('revenue_growth', 0)
        profit_growth = data.get('profit_growth', 0)
        momentum_20d = data.get('momentum_20d', 0)
        momentum_60d = data.get('momentum_60d', 0)
        vol_ratio = data.get('vol_ratio', 1)
        pe = data.get('pe', 50)
        market_cap = data.get('market_cap', 100)  # 亿
        
        # S4加速期: 业绩爆发，估值修复
        if revenue_growth > 80 and profit_growth > 100 and momentum_60d > 50:
            signals.append("业绩拐点确认")
            signals.append("估值快速修复")
            return Stage.S4, 0.85, signals
        
        # S3放量期: 批量订单，扩产
        if revenue_growth > 50 and profit_growth > 60 and vol_ratio > 1.5:
            signals.append("营收高速增长")
            signals.append("放量上涨")
            if momentum_20d > 15:
                return Stage.S3, 0.80, signals
        
        # S2导入期 (最佳买点): 小批量验证通过
        if 30 <= revenue_growth <= 60 and 20 <= profit_growth <= 60:
            if momentum_20d > 5 and market_cap < 300:
                signals.append("成长黄金期")
                signals.append("市值适中")
                return Stage.S2, 0.75, signals
        
        # S1验证期: 有增长但未放量
        if 15 <= revenue_growth < 40 and profit_growth > 10:
            signals.append("增长验证中")
            return Stage.S1, 0.60, signals
        
        # S5成熟期: 大市值，低增速
        if market_cap > 1000 and revenue_growth < 15:
            signals.append("增长放缓")
            return Stage.S5, 0.70, signals
        
        # S0观察期
        signals.append("待进一步验证")
        return Stage.S0, 0.40, signals


# ============================================================
# 多因子打分系统
# ============================================================

class MultifactorScorer:
    """多因子打分系统"""
    
    # 因子权重
    FACTOR_WEIGHTS = {
        # 基本面因子 (40%)
        'roe': 0.08,
        'revenue_growth': 0.10,
        'profit_growth': 0.08,
        'gross_margin': 0.06,
        'rd_ratio': 0.08,
        
        # 估值因子 (15%)
        'pe_score': 0.08,
        'pb_score': 0.07,
        
        # 技术因子 (25%)
        'momentum_20d': 0.10,
        'momentum_60d': 0.08,
        'vol_ratio': 0.07,
        
        # 阶段因子 (20%)
        'stage_score': 0.20,
    }
    
    def __init__(self):
        self.stage_identifier = StageIdentifier()
        self.scorecard_engine = ScoreCardEngine()
    
    def score(self, symbol: str, name: str, data: Dict) -> Dict:
        """计算综合得分"""
        
        # 1. 阶段识别
        stage, stage_confidence, stage_signals = self.stage_identifier.identify(data)
        stage_score = STAGE_WEIGHTS.get(stage, 0.2) * 100
        
        # 2. 评分卡
        scorecard = self.scorecard_engine.compute(symbol, name, data)
        
        # 3. 因子得分
        factor_scores = {}
        
        # 基本面因子
        factor_scores['roe'] = min(100, max(0, data.get('roe', 0) * 5))
        factor_scores['revenue_growth'] = min(100, max(0, data.get('revenue_growth', 0) * 2))
        factor_scores['profit_growth'] = min(100, max(0, data.get('profit_growth', 0) * 1.5))
        factor_scores['gross_margin'] = min(100, max(0, data.get('gross_margin', 0) * 2))
        factor_scores['rd_ratio'] = min(100, max(0, data.get('rd_ratio', 0) * 10))
        
        # 估值因子 (低PE/PB得高分)
        pe = data.get('pe', 50)
        factor_scores['pe_score'] = max(0, 100 - pe * 1.5) if pe > 0 else 50
        
        pb = data.get('pb', 3)
        factor_scores['pb_score'] = max(0, 100 - pb * 20) if pb > 0 else 50
        
        # 技术因子
        factor_scores['momentum_20d'] = min(100, max(0, 50 + data.get('momentum_20d', 0) * 2))
        factor_scores['momentum_60d'] = min(100, max(0, 50 + data.get('momentum_60d', 0)))
        factor_scores['vol_ratio'] = min(100, max(0, data.get('vol_ratio', 1) * 40))
        
        # 阶段因子
        factor_scores['stage_score'] = stage_score
        
        # 4. 计算加权总分
        total_score = sum(
            factor_scores.get(k, 50) * self.FACTOR_WEIGHTS[k]
            for k in self.FACTOR_WEIGHTS
        )
        
        # 5. 科技主线加成
        tech_bonus = 0
        industry = data.get('industry', '')
        for keyword in TECH_KEYWORDS:
            if keyword in industry or keyword in name:
                tech_bonus = 10
                break
        
        total_score = min(100, total_score + tech_bonus)
        
        return {
            'symbol': symbol,
            'name': name,
            'total_score': round(total_score, 1),
            'stage': stage.value,
            'stage_confidence': stage_confidence,
            'stage_signals': stage_signals,
            'scorecard_grade': scorecard.grade,
            'scorecard_score': scorecard.total_score,
            'scorecard_signals': scorecard.signals,
            'factor_scores': factor_scores,
            'tech_bonus': tech_bonus,
            'recommendation': self._get_recommendation(total_score, stage)
        }
    
    def _get_recommendation(self, score: float, stage: Stage) -> str:
        """生成推荐"""
        if score >= 80 and stage in [Stage.S1, Stage.S2]:
            return "强烈推荐 - 早期布局良机"
        elif score >= 70 and stage in [Stage.S2, Stage.S3]:
            return "推荐 - 成长黄金期"
        elif score >= 60:
            return "关注 - 等待更好时机"
        elif score >= 50:
            return "观察 - 需更多验证"
        else:
            return "不推荐"


# ============================================================
# 波段操作引擎
# ============================================================

class SwingTradeEngine:
    """波段操作引擎"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.max_holdings = self.config.get('max_holdings', 5)
        self.stop_loss = self.config.get('stop_loss', -0.10)
        self.take_profit = self.config.get('take_profit', 0.50)
        self.trailing_stop = self.config.get('trailing_stop', 0.15)
        self.min_score = self.config.get('min_score', 70)
    
    def generate_signals(self, candidates: List[Dict], current_positions: Dict) -> List[Dict]:
        """
        生成交易信号
        
        Args:
            candidates: 候选股票列表 (已按得分排序)
            current_positions: 当前持仓 {symbol: {shares, cost, highest_price}}
        
        Returns:
            交易信号列表
        """
        signals = []
        
        # 1. 检查卖出信号
        for symbol, pos in current_positions.items():
            cost = pos['cost']
            current_price = pos.get('current_price', cost)
            highest_price = pos.get('highest_price', current_price)
            
            pnl = (current_price - cost) / cost
            drawdown_from_high = (current_price - highest_price) / highest_price if highest_price > 0 else 0
            
            # 止损
            if pnl <= self.stop_loss:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'止损 ({pnl*100:.1f}%)',
                    'priority': 1
                })
                continue
            
            # 止盈
            if pnl >= self.take_profit:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'止盈 ({pnl*100:.1f}%)',
                    'priority': 2
                })
                continue
            
            # 移动止损
            if drawdown_from_high <= -self.trailing_stop:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'移动止损 (从高点回撤 {drawdown_from_high*100:.1f}%)',
                    'priority': 3
                })
        
        # 2. 检查买入信号
        current_count = len(current_positions) - sum(1 for s in signals if s['action'] == 'SELL')
        slots_available = self.max_holdings - current_count
        
        if slots_available > 0:
            for candidate in candidates:
                if len([s for s in signals if s['action'] == 'BUY']) >= slots_available:
                    break
                
                symbol = candidate['symbol']
                
                # 跳过已持有
                if symbol in current_positions:
                    continue
                
                # 检查得分
                if candidate['total_score'] < self.min_score:
                    continue
                
                # 只在S1-S3阶段买入
                stage = candidate.get('stage', 'S0')
                if stage not in ['S1', 'S2', 'S3']:
                    continue
                
                signals.append({
                    'symbol': symbol,
                    'name': candidate.get('name', ''),
                    'action': 'BUY',
                    'reason': f"得分 {candidate['total_score']:.1f}, 阶段 {stage}",
                    'score': candidate['total_score'],
                    'stage': stage,
                    'priority': 10 - int(candidate['total_score'] / 10)  # 高分优先
                })
        
        # 按优先级排序
        signals.sort(key=lambda x: x['priority'])
        
        return signals


# ============================================================
# 主系统
# ============================================================

class TenbaggerMultifactorSystem:
    """十倍股多因子量化系统"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.jqdata_username = self.config.get('jqdata_username', '13327806797')
        self.scorer = MultifactorScorer()
        self.swing_engine = SwingTradeEngine(self.config)
        self.jq_authenticated = False
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth(self.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def get_tech_universe(self) -> List[str]:
        """获取科技主线股票池"""
        # 中证科技100 + 创业板指成分股
        stocks = []
        
        try:
            # 创业板
            stocks += jq.get_index_stocks('399006.XSHE')[:50]
            # 科创50
            stocks += jq.get_index_stocks('000688.XSHG')[:30] if jq.get_index_stocks('000688.XSHG') else []
            # 中证500中的科技股 (通过行业筛选)
            zz500 = jq.get_index_stocks('000905.XSHG')
            
            # 筛选科技行业
            for stock in zz500[:100]:
                try:
                    info = jq.get_security_info(stock)
                    if info and any(kw in info.display_name for kw in TECH_KEYWORDS):
                        stocks.append(stock)
                except:
                    continue
        except:
            pass
        
        return list(set(stocks))
    
    def fetch_stock_data(self, stock: str, date: str) -> Dict:
        """获取股票数据"""
        data = {'symbol': stock}
        
        try:
            # 基本信息
            info = jq.get_security_info(stock)
            if info:
                data['name'] = info.display_name
            
            # 基本面数据
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.market_cap,
                jq.indicator.roe,
                jq.indicator.roa,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin
            ).filter(jq.valuation.code == stock)
            
            fund_df = jq.get_fundamentals(q, date=date)
            
            if not fund_df.empty:
                data['pe'] = fund_df['pe_ratio'].iloc[0] or 50
                data['pb'] = fund_df['pb_ratio'].iloc[0] or 3
                data['market_cap'] = (fund_df['market_cap'].iloc[0] or 100) / 100000000  # 转亿
                data['roe'] = fund_df['roe'].iloc[0] or 0
                data['roa'] = fund_df['roa'].iloc[0] or 0
                data['revenue_growth'] = fund_df['inc_revenue_year_on_year'].iloc[0] or 0
                data['profit_growth'] = fund_df['inc_net_profit_year_on_year'].iloc[0] or 0
                data['gross_margin'] = fund_df['gross_profit_margin'].iloc[0] or 0
            
            # 技术数据
            price_df = jq.get_price(
                stock, end_date=date, count=60,
                frequency='daily', fields=['close', 'volume']
            )
            
            if price_df is not None and len(price_df) >= 60:
                close = price_df['close'].values
                volume = price_df['volume'].values
                
                data['momentum_5d'] = (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0
                data['momentum_20d'] = (close[-1] / close[-20] - 1) * 100 if close[-20] > 0 else 0
                data['momentum_60d'] = (close[-1] / close[0] - 1) * 100 if close[0] > 0 else 0
                data['vol_ratio'] = np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1
                data['current_price'] = close[-1]
            
            # 行业
            try:
                ind = jq.get_industry(stock, date=date)
                if ind and stock in ind:
                    data['industry'] = ind[stock].get('sw_l1', {}).get('industry_name', '')
            except:
                data['industry'] = ''
            
        except Exception as e:
            logger.warning(f"获取{stock}数据失败: {e}")
        
        return data
    
    def scan_and_score(self, date: str = None) -> List[Dict]:
        """扫描并打分"""
        if not self.authenticate_jqdata():
            return []
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📊 开始扫描 ({date})...")
        
        # 获取股票池
        universe = self.get_tech_universe()
        logger.info(f"   股票池: {len(universe)}只")
        
        # 扫描并打分
        results = []
        for i, stock in enumerate(universe):
            if i % 20 == 0:
                logger.info(f"   进度: {i}/{len(universe)}")
            
            data = self.fetch_stock_data(stock, date)
            if data.get('name'):
                score_result = self.scorer.score(stock, data.get('name', ''), data)
                score_result['data'] = data
                results.append(score_result)
        
        # 按得分排序
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        logger.info(f"✅ 扫描完成: {len(results)}只股票")
        
        return results
    
    def get_top_candidates(self, results: List[Dict], top_n: int = 5) -> List[Dict]:
        """获取Top候选"""
        # 只保留S1-S3阶段的高分股票
        filtered = [
            r for r in results
            if r['total_score'] >= 70 and r.get('stage', 'S0') in ['S1', 'S2', 'S3']
        ]
        
        return filtered[:top_n]
    
    def run_backtest(self, start_date: str, end_date: str, initial_capital: float = 1000000) -> Dict:
        """运行回测"""
        if not self.authenticate_jqdata():
            return {'success': False, 'error': 'JQData认证失败'}
        
        logger.info(f"🚀 开始回测: {start_date} ~ {end_date}")
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [str(d) for d in trade_days]
        
        # 获取股票池
        universe = self.get_tech_universe()[:50]  # 限制数量
        
        # 预加载价格数据
        logger.info("   预加载价格数据...")
        price_df = jq.get_price(
            universe,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None:
            for stock in universe:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        # 初始化
        cash = initial_capital
        positions = {}
        equity_curve = [cash]
        trades = []
        
        rebalance_days = self.config.get('rebalance_days', 10)
        counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
            
            # 更新持仓价值和最高价
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    current_price = price_cache[stock].loc[date, 'close']
                    pos['current_price'] = current_price
                    pos['highest_price'] = max(pos.get('highest_price', current_price), current_price)
                    portfolio_value += pos['shares'] * current_price
            
            # 调仓检查
            counter += 1
            if counter >= rebalance_days:
                counter = 0
                
                # 简化版: 基于动量和价格位置打分
                scores = {}
                for stock in universe:
                    if stock in price_cache:
                        try:
                            sdf = price_cache[stock]
                            mask = sdf.index <= date
                            sdf = sdf[mask].tail(60)
                            
                            if len(sdf) >= 60:
                                close = sdf['close'].values
                                
                                momentum_20d = (close[-1] / close[-20] - 1) * 100
                                momentum_60d = (close[-1] / close[0] - 1) * 100
                                price_to_ma20 = (close[-1] / np.mean(close[-20:]) - 1) * 100
                                
                                # 简化打分
                                score = 50 + momentum_20d * 0.5 + momentum_60d * 0.3
                                if price_to_ma20 > 0:
                                    score += 10
                                
                                if score >= self.swing_engine.min_score:
                                    scores[stock] = score
                        except:
                            continue
                
                candidates = [
                    {'symbol': s, 'total_score': sc, 'stage': 'S2', 'name': ''}
                    for s, sc in sorted(scores.items(), key=lambda x: x[1], reverse=True)
                ]
                
                # 生成交易信号
                signals = self.swing_engine.generate_signals(candidates, positions)
                
                # 执行交易
                for signal in signals:
                    stock = signal['symbol']
                    
                    if signal['action'] == 'SELL' and stock in positions:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            value = positions[stock]['shares'] * price * 0.9985  # 扣费
                            cash += value
                            trades.append({
                                'date': date,
                                'symbol': stock,
                                'action': 'SELL',
                                'price': price,
                                'shares': positions[stock]['shares'],
                                'reason': signal['reason']
                            })
                            del positions[stock]
                    
                    elif signal['action'] == 'BUY' and stock not in positions:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            target_value = portfolio_value / self.swing_engine.max_holdings
                            buy_value = min(target_value, cash)
                            shares = int(buy_value / price / 100) * 100
                            
                            if shares > 0:
                                cost = shares * price * 1.0003  # 扣费
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {
                                        'shares': shares,
                                        'cost': price,
                                        'highest_price': price,
                                        'current_price': price
                                    }
                                    trades.append({
                                        'date': date,
                                        'symbol': stock,
                                        'action': 'BUY',
                                        'price': price,
                                        'shares': shares,
                                        'reason': signal['reason']
                                    })
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
            
            equity_curve.append(portfolio_value)
        
        # 计算指标
        equity = pd.Series(equity_curve)
        returns = equity.pct_change().fillna(0)
        
        total_return = (equity.iloc[-1] / initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        calmar = annual_return / max_dd if max_dd > 0 else 0
        
        logger.info(f"✅ 回测完成")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化收益: {annual_return*100:.2f}%")
        logger.info(f"   夏普比率: {sharpe:.2f}")
        logger.info(f"   最大回撤: {max_dd*100:.2f}%")
        
        return {
            'success': True,
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'calmar_ratio': calmar,
                'max_drawdown': max_dd,
                'volatility': volatility
            },
            'equity_curve': equity_curve,
            'trades': trades,
            'trade_count': len(trades)
        }
    
    def generate_report(self, scan_results: List[Dict], backtest_results: Dict) -> str:
        """生成HTML报告"""
        metrics = backtest_results.get('metrics', {})
        top_candidates = self.get_top_candidates(scan_results, 5)
        
        # 生成图表
        chart_html = ""
        if MATPLOTLIB_AVAILABLE and backtest_results.get('equity_curve'):
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            equity = backtest_results['equity_curve']
            axes[0].plot(equity, linewidth=2, color='#667eea')
            axes[0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#667eea')
            axes[0].set_title('Portfolio Value', fontweight='bold')
            axes[0].grid(True, alpha=0.3)
            
            # 回撤
            equity_s = pd.Series(equity)
            peak = equity_s.cummax()
            dd = (equity_s - peak) / peak
            axes[1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
            axes[1].set_title('Drawdown (%)', fontweight='bold')
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            chart_b64 = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股多因子量化系统报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; padding: 30px; margin: 0; min-height: 100vh; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; box-shadow: 0 20px 60px rgba(102,126,234,0.3); }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }}
        .header p {{ margin: 8px 0; opacity: 0.9; font-size: 1.1em; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }}
        .metric .value {{ font-size: 2.5em; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .metric .value.positive {{ background: linear-gradient(135deg, #4ade80, #22c55e); -webkit-background-clip: text; }}
        .metric .value.negative {{ background: linear-gradient(135deg, #f87171, #ef4444); -webkit-background-clip: text; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; backdrop-filter: blur(10px); }}
        .section h2 {{ color: #667eea; margin-top: 0; font-size: 1.6em; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 15px; }}
        .chart {{ text-align: center; margin: 25px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); font-weight: 600; }}
        tr:hover {{ background: rgba(102,126,234,0.1); }}
        .tag {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 0.85em; margin: 3px; }}
        .tag-s {{ background: linear-gradient(135deg, #4ade80, #22c55e); color: white; }}
        .tag-a {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
        .tag-stage {{ background: rgba(251,191,36,0.2); color: #fbbf24; }}
        .highlight {{ color: #4ade80; font-weight: bold; }}
        .stock-card {{ background: rgba(255,255,255,0.05); border-radius: 16px; padding: 25px; margin: 15px 0; border-left: 4px solid #667eea; }}
        .stock-card h3 {{ margin: 0 0 15px 0; color: #667eea; }}
        .signals {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股多因子量化系统</h1>
            <p>整合阶段识别 | 7维评分卡 | 多因子打分 | 科技主线聚焦</p>
            <p>目标：聚焦5只以内股票，波段操作，控制回撤</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">交易次数</div>
                <div class="value">{backtest_results.get('trade_count', 0)}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        <div class="section">
            <h2>🎯 Top 5 候选股票</h2>
            {''.join([f'''
            <div class="stock-card">
                <h3>{c.get('name', '')} ({c.get('symbol', '')})</h3>
                <p><span class="tag tag-{'s' if c.get('scorecard_grade','C') in ['S+','S'] else 'a'}">评分: {c.get('total_score', 0):.1f}</span>
                   <span class="tag tag-stage">阶段: {c.get('stage', 'S0')}</span>
                   <span class="tag">推荐: {c.get('recommendation', '')}</span></p>
                <div class="signals">
                    {''.join([f'<span class="tag" style="background:rgba(74,222,128,0.2);color:#4ade80">{s}</span>' for s in c.get('stage_signals', [])[:3]])}
                    {''.join([f'<span class="tag" style="background:rgba(102,126,234,0.2);color:#667eea">{s}</span>' for s in c.get('scorecard_signals', [])[:3]])}
                </div>
            </div>
            ''' for c in top_candidates])}
        </div>
        
        <div class="section">
            <h2>📋 系统说明</h2>
            <table>
                <tr><th>模块</th><th>说明</th></tr>
                <tr><td>阶段识别</td><td>S0(观察)→S1(验证)→S2(导入,最佳买点)→S3(放量)→S4(加速)→S5(成熟)</td></tr>
                <tr><td>7维评分卡</td><td>盈利能力/成长性/财务健康/估值水平/行业地位/管理质量/市场表现</td></tr>
                <tr><td>多因子打分</td><td>基本面(40%)+估值(15%)+技术(25%)+阶段(20%)</td></tr>
                <tr><td>科技主线</td><td>AI/半导体/新能源/量子计算/生物医药</td></tr>
                <tr><td>波段操作</td><td>止损{self.swing_engine.stop_loss*100:.0f}%/止盈{self.swing_engine.take_profit*100:.0f}%/移动止损{self.swing_engine.trailing_stop*100:.0f}%</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
        
        return html


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股多因子量化系统")
    logger.info("=" * 80)
    
    # 配置
    config = {
        'jqdata_username': '13327806797',
        'max_holdings': 5,
        'stop_loss': -0.10,
        'take_profit': 0.50,
        'trailing_stop': 0.15,
        'min_score': 65,
        'rebalance_days': 10,
    }
    
    # 创建系统
    system = TenbaggerMultifactorSystem(config)
    
    # 1. 扫描并打分
    scan_date = datetime.now().strftime('%Y-%m-%d')
    scan_results = system.scan_and_score(scan_date)
    
    # 2. 回测
    backtest_results = system.run_backtest(
        start_date="2024-01-01",
        end_date="2025-12-20",
        initial_capital=1000000
    )
    
    # 3. 生成报告
    logger.info("📝 生成报告...")
    html = system.generate_report(scan_results, backtest_results)
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_multifactor_system_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告已保存: {report_path}")
    
    # 登出
    jq.logout()
    
    # 打印Top候选
    logger.info("\n🎯 Top 5 候选股票:")
    for c in system.get_top_candidates(scan_results, 5):
        logger.info(f"   {c['name']} ({c['symbol']}): 得分 {c['total_score']:.1f}, 阶段 {c['stage']}")
    
    logger.info("=" * 80)
    
    return {
        'scan_results': scan_results,
        'backtest_results': backtest_results,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()



# -*- coding: utf-8 -*-
"""
十倍股多因子量化系统 - 早期识别与波段操作
==========================================

整合知识库核心逻辑：
1. 阶段识别系统（S0-S5）
2. 7维评分卡
3. 多因子打分模型
4. 科技主线识别
5. 波段操作+回撤控制

目标：聚焦5只以内股票，获取10倍以上回报

代码位置: research/tenbagger_10x_strategy/scripts/tenbagger_multifactor_system.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json
import logging
import base64
from io import BytesIO
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

import jqdatasdk as jq


# ============================================================
# 阶段定义
# ============================================================

class Stage(Enum):
    """十倍股成长阶段"""
    S0 = "S0"  # 观察期 - 有产业链位置，无明显兑现信号
    S1 = "S1"  # 验证期 - 送样/认证中，尚未确认客户
    S2 = "S2"  # 导入期 - 已进入客户体系，最佳介入点
    S3 = "S3"  # 放量期 - 批量订单，扩产明确
    S4 = "S4"  # 加速期 - 业绩拐点，估值修复
    S5 = "S5"  # 成熟期 - 主流共识，十倍股特征消失


STAGE_WEIGHTS = {
    Stage.S0: 0.2,
    Stage.S1: 0.5,
    Stage.S2: 1.0,  # 最佳介入
    Stage.S3: 0.8,
    Stage.S4: 0.4,
    Stage.S5: 0.1,
}


# ============================================================
# 科技主线板块
# ============================================================

TECH_MAINLINE_INDUSTRIES = {
    # AI人工智能
    "AI芯片": ["算力", "GPU", "NPU", "ASIC"],
    "AI算法": ["大模型", "机器学习", "深度学习"],
    "AI应用": ["智能驾驶", "机器人", "具身智能"],
    
    # 半导体
    "半导体设备": ["光刻", "刻蚀", "薄膜沉积", "离子注入"],
    "半导体材料": ["光刻胶", "特种气体", "靶材", "CMP"],
    "芯片设计": ["CPU", "GPU", "存储芯片", "MCU"],
    
    # 新能源
    "锂电池": ["正极材料", "负极材料", "隔膜", "电解液"],
    "光伏": ["硅料", "硅片", "电池片", "组件"],
    "储能": ["储能系统", "逆变器", "BMS"],
    
    # 其他高科技
    "量子计算": ["量子芯片", "量子通信"],
    "生物医药": ["创新药", "CXO", "医疗器械"],
}

TECH_KEYWORDS = [
    "AI", "人工智能", "大模型", "算力", "芯片", "半导体", "GPU", "CPU",
    "机器人", "自动驾驶", "智能驾驶", "新能源", "锂电", "光伏", "储能",
    "量子", "生物医药", "创新药", "5G", "6G", "物联网", "边缘计算"
]


# ============================================================
# 7维评分卡
# ============================================================

@dataclass
class ScorecardResult:
    """评分卡结果"""
    symbol: str
    name: str
    total_score: float
    grade: str
    dimensions: Dict[str, float]
    signals: List[str]


class ScoreCardEngine:
    """7维评分卡引擎"""
    
    # 维度权重
    DIMENSION_WEIGHTS = {
        "profitability": 0.15,      # 盈利能力
        "growth": 0.20,             # 成长性
        "financial_health": 0.10,   # 财务健康
        "valuation": 0.15,          # 估值水平
        "industry_position": 0.15,  # 行业地位
        "management": 0.10,         # 管理质量
        "market_performance": 0.15, # 市场表现
    }
    
    def compute(self, symbol: str, name: str, data: Dict) -> ScorecardResult:
        """计算评分"""
        scores = {}
        signals = []
        
        # 1. 盈利能力
        roe = data.get('roe', 0)
        gross_margin = data.get('gross_margin', 0)
        
        profitability_score = 0
        if roe > 20:
            profitability_score = 100
            signals.append(f"ROE极高({roe:.1f}%)")
        elif roe > 15:
            profitability_score = 80
        elif roe > 10:
            profitability_score = 60
        elif roe > 5:
            profitability_score = 40
        else:
            profitability_score = 20
        
        if gross_margin > 40:
            profitability_score = min(100, profitability_score + 20)
            signals.append(f"毛利率高({gross_margin:.1f}%)")
        
        scores['profitability'] = profitability_score
        
        # 2. 成长性
        revenue_growth = data.get('revenue_growth', 0)
        profit_growth = data.get('profit_growth', 0)
        
        growth_score = 0
        if revenue_growth > 50:
            growth_score = 100
            signals.append(f"营收高增长({revenue_growth:.0f}%)")
        elif revenue_growth > 30:
            growth_score = 80
        elif revenue_growth > 15:
            growth_score = 60
        elif revenue_growth > 0:
            growth_score = 40
        else:
            growth_score = 20
        
        if profit_growth > 50:
            growth_score = min(100, growth_score + 20)
            signals.append(f"利润高增长({profit_growth:.0f}%)")
        
        scores['growth'] = growth_score
        
        # 3. 财务健康
        debt_ratio = data.get('debt_ratio', 50)
        current_ratio = data.get('current_ratio', 1)
        
        health_score = 0
        if debt_ratio < 30:
            health_score = 100
        elif debt_ratio < 50:
            health_score = 80
        elif debt_ratio < 70:
            health_score = 60
        else:
            health_score = 40
        
        if current_ratio > 2:
            health_score = min(100, health_score + 10)
        
        scores['financial_health'] = health_score
        
        # 4. 估值水平
        pe = data.get('pe', 50)
        pb = data.get('pb', 3)
        
        valuation_score = 0
        if 0 < pe < 20:
            valuation_score = 100
            signals.append(f"估值合理(PE={pe:.0f})")
        elif 20 <= pe < 40:
            valuation_score = 70
        elif 40 <= pe < 80:
            valuation_score = 50
        else:
            valuation_score = 30
        
        scores['valuation'] = valuation_score
        
        # 5. 行业地位
        market_share = data.get('market_share', 0)
        is_leader = data.get('is_leader', False)
        
        industry_score = 50  # 默认中等
        if is_leader:
            industry_score = 90
            signals.append("行业龙头")
        elif market_share > 10:
            industry_score = 70
        
        scores['industry_position'] = industry_score
        
        # 6. 管理质量
        rd_ratio = data.get('rd_ratio', 0)  # 研发投入占比
        
        management_score = 50
        if rd_ratio > 10:
            management_score = 90
            signals.append(f"研发投入高({rd_ratio:.1f}%)")
        elif rd_ratio > 5:
            management_score = 70
        
        scores['management'] = management_score
        
        # 7. 市场表现
        momentum_20d = data.get('momentum_20d', 0)
        momentum_60d = data.get('momentum_60d', 0)
        vol_ratio = data.get('vol_ratio', 1)
        
        market_score = 50
        if momentum_20d > 20 and momentum_60d > 30:
            market_score = 90
            signals.append("强势动量")
        elif momentum_20d > 10:
            market_score = 70
        elif momentum_20d < -10:
            market_score = 30
        
        if vol_ratio > 2:
            market_score = min(100, market_score + 10)
            signals.append("放量突破")
        
        scores['market_performance'] = market_score
        
        # 计算总分
        total_score = sum(scores[k] * self.DIMENSION_WEIGHTS[k] for k in scores)
        
        # 确定等级
        if total_score >= 85:
            grade = "S+"
        elif total_score >= 75:
            grade = "S"
        elif total_score >= 65:
            grade = "A"
        elif total_score >= 50:
            grade = "B"
        elif total_score >= 35:
            grade = "C"
        else:
            grade = "D"
        
        return ScorecardResult(
            symbol=symbol,
            name=name,
            total_score=total_score,
            grade=grade,
            dimensions=scores,
            signals=signals
        )


# ============================================================
# 阶段识别引擎
# ============================================================

class StageIdentifier:
    """阶段识别引擎"""
    
    def identify(self, data: Dict) -> Tuple[Stage, float, List[str]]:
        """
        识别股票所处阶段
        
        Returns:
            (阶段, 置信度, 信号列表)
        """
        signals = []
        
        revenue_growth = data.get('revenue_growth', 0)
        profit_growth = data.get('profit_growth', 0)
        momentum_20d = data.get('momentum_20d', 0)
        momentum_60d = data.get('momentum_60d', 0)
        vol_ratio = data.get('vol_ratio', 1)
        pe = data.get('pe', 50)
        market_cap = data.get('market_cap', 100)  # 亿
        
        # S4加速期: 业绩爆发，估值修复
        if revenue_growth > 80 and profit_growth > 100 and momentum_60d > 50:
            signals.append("业绩拐点确认")
            signals.append("估值快速修复")
            return Stage.S4, 0.85, signals
        
        # S3放量期: 批量订单，扩产
        if revenue_growth > 50 and profit_growth > 60 and vol_ratio > 1.5:
            signals.append("营收高速增长")
            signals.append("放量上涨")
            if momentum_20d > 15:
                return Stage.S3, 0.80, signals
        
        # S2导入期 (最佳买点): 小批量验证通过
        if 30 <= revenue_growth <= 60 and 20 <= profit_growth <= 60:
            if momentum_20d > 5 and market_cap < 300:
                signals.append("成长黄金期")
                signals.append("市值适中")
                return Stage.S2, 0.75, signals
        
        # S1验证期: 有增长但未放量
        if 15 <= revenue_growth < 40 and profit_growth > 10:
            signals.append("增长验证中")
            return Stage.S1, 0.60, signals
        
        # S5成熟期: 大市值，低增速
        if market_cap > 1000 and revenue_growth < 15:
            signals.append("增长放缓")
            return Stage.S5, 0.70, signals
        
        # S0观察期
        signals.append("待进一步验证")
        return Stage.S0, 0.40, signals


# ============================================================
# 多因子打分系统
# ============================================================

class MultifactorScorer:
    """多因子打分系统"""
    
    # 因子权重
    FACTOR_WEIGHTS = {
        # 基本面因子 (40%)
        'roe': 0.08,
        'revenue_growth': 0.10,
        'profit_growth': 0.08,
        'gross_margin': 0.06,
        'rd_ratio': 0.08,
        
        # 估值因子 (15%)
        'pe_score': 0.08,
        'pb_score': 0.07,
        
        # 技术因子 (25%)
        'momentum_20d': 0.10,
        'momentum_60d': 0.08,
        'vol_ratio': 0.07,
        
        # 阶段因子 (20%)
        'stage_score': 0.20,
    }
    
    def __init__(self):
        self.stage_identifier = StageIdentifier()
        self.scorecard_engine = ScoreCardEngine()
    
    def score(self, symbol: str, name: str, data: Dict) -> Dict:
        """计算综合得分"""
        
        # 1. 阶段识别
        stage, stage_confidence, stage_signals = self.stage_identifier.identify(data)
        stage_score = STAGE_WEIGHTS.get(stage, 0.2) * 100
        
        # 2. 评分卡
        scorecard = self.scorecard_engine.compute(symbol, name, data)
        
        # 3. 因子得分
        factor_scores = {}
        
        # 基本面因子
        factor_scores['roe'] = min(100, max(0, data.get('roe', 0) * 5))
        factor_scores['revenue_growth'] = min(100, max(0, data.get('revenue_growth', 0) * 2))
        factor_scores['profit_growth'] = min(100, max(0, data.get('profit_growth', 0) * 1.5))
        factor_scores['gross_margin'] = min(100, max(0, data.get('gross_margin', 0) * 2))
        factor_scores['rd_ratio'] = min(100, max(0, data.get('rd_ratio', 0) * 10))
        
        # 估值因子 (低PE/PB得高分)
        pe = data.get('pe', 50)
        factor_scores['pe_score'] = max(0, 100 - pe * 1.5) if pe > 0 else 50
        
        pb = data.get('pb', 3)
        factor_scores['pb_score'] = max(0, 100 - pb * 20) if pb > 0 else 50
        
        # 技术因子
        factor_scores['momentum_20d'] = min(100, max(0, 50 + data.get('momentum_20d', 0) * 2))
        factor_scores['momentum_60d'] = min(100, max(0, 50 + data.get('momentum_60d', 0)))
        factor_scores['vol_ratio'] = min(100, max(0, data.get('vol_ratio', 1) * 40))
        
        # 阶段因子
        factor_scores['stage_score'] = stage_score
        
        # 4. 计算加权总分
        total_score = sum(
            factor_scores.get(k, 50) * self.FACTOR_WEIGHTS[k]
            for k in self.FACTOR_WEIGHTS
        )
        
        # 5. 科技主线加成
        tech_bonus = 0
        industry = data.get('industry', '')
        for keyword in TECH_KEYWORDS:
            if keyword in industry or keyword in name:
                tech_bonus = 10
                break
        
        total_score = min(100, total_score + tech_bonus)
        
        return {
            'symbol': symbol,
            'name': name,
            'total_score': round(total_score, 1),
            'stage': stage.value,
            'stage_confidence': stage_confidence,
            'stage_signals': stage_signals,
            'scorecard_grade': scorecard.grade,
            'scorecard_score': scorecard.total_score,
            'scorecard_signals': scorecard.signals,
            'factor_scores': factor_scores,
            'tech_bonus': tech_bonus,
            'recommendation': self._get_recommendation(total_score, stage)
        }
    
    def _get_recommendation(self, score: float, stage: Stage) -> str:
        """生成推荐"""
        if score >= 80 and stage in [Stage.S1, Stage.S2]:
            return "强烈推荐 - 早期布局良机"
        elif score >= 70 and stage in [Stage.S2, Stage.S3]:
            return "推荐 - 成长黄金期"
        elif score >= 60:
            return "关注 - 等待更好时机"
        elif score >= 50:
            return "观察 - 需更多验证"
        else:
            return "不推荐"


# ============================================================
# 波段操作引擎
# ============================================================

class SwingTradeEngine:
    """波段操作引擎"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.max_holdings = self.config.get('max_holdings', 5)
        self.stop_loss = self.config.get('stop_loss', -0.10)
        self.take_profit = self.config.get('take_profit', 0.50)
        self.trailing_stop = self.config.get('trailing_stop', 0.15)
        self.min_score = self.config.get('min_score', 70)
    
    def generate_signals(self, candidates: List[Dict], current_positions: Dict) -> List[Dict]:
        """
        生成交易信号
        
        Args:
            candidates: 候选股票列表 (已按得分排序)
            current_positions: 当前持仓 {symbol: {shares, cost, highest_price}}
        
        Returns:
            交易信号列表
        """
        signals = []
        
        # 1. 检查卖出信号
        for symbol, pos in current_positions.items():
            cost = pos['cost']
            current_price = pos.get('current_price', cost)
            highest_price = pos.get('highest_price', current_price)
            
            pnl = (current_price - cost) / cost
            drawdown_from_high = (current_price - highest_price) / highest_price if highest_price > 0 else 0
            
            # 止损
            if pnl <= self.stop_loss:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'止损 ({pnl*100:.1f}%)',
                    'priority': 1
                })
                continue
            
            # 止盈
            if pnl >= self.take_profit:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'止盈 ({pnl*100:.1f}%)',
                    'priority': 2
                })
                continue
            
            # 移动止损
            if drawdown_from_high <= -self.trailing_stop:
                signals.append({
                    'symbol': symbol,
                    'action': 'SELL',
                    'reason': f'移动止损 (从高点回撤 {drawdown_from_high*100:.1f}%)',
                    'priority': 3
                })
        
        # 2. 检查买入信号
        current_count = len(current_positions) - sum(1 for s in signals if s['action'] == 'SELL')
        slots_available = self.max_holdings - current_count
        
        if slots_available > 0:
            for candidate in candidates:
                if len([s for s in signals if s['action'] == 'BUY']) >= slots_available:
                    break
                
                symbol = candidate['symbol']
                
                # 跳过已持有
                if symbol in current_positions:
                    continue
                
                # 检查得分
                if candidate['total_score'] < self.min_score:
                    continue
                
                # 只在S1-S3阶段买入
                stage = candidate.get('stage', 'S0')
                if stage not in ['S1', 'S2', 'S3']:
                    continue
                
                signals.append({
                    'symbol': symbol,
                    'name': candidate.get('name', ''),
                    'action': 'BUY',
                    'reason': f"得分 {candidate['total_score']:.1f}, 阶段 {stage}",
                    'score': candidate['total_score'],
                    'stage': stage,
                    'priority': 10 - int(candidate['total_score'] / 10)  # 高分优先
                })
        
        # 按优先级排序
        signals.sort(key=lambda x: x['priority'])
        
        return signals


# ============================================================
# 主系统
# ============================================================

class TenbaggerMultifactorSystem:
    """十倍股多因子量化系统"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.jqdata_username = self.config.get('jqdata_username', '13327806797')
        self.scorer = MultifactorScorer()
        self.swing_engine = SwingTradeEngine(self.config)
        self.jq_authenticated = False
    
    def authenticate_jqdata(self) -> bool:
        """认证JQData"""
        if self.jq_authenticated:
            return True
        
        try:
            cfg_path = PROJECT_ROOT / "config" / f"jqdata_{self.jqdata_username}.json"
            if cfg_path.exists():
                with open(cfg_path, 'r') as f:
                    pwd = json.load(f).get('password')
            jq.auth(self.jqdata_username, pwd)
            self.jq_authenticated = True
            logger.info("✅ JQData认证成功")
            return True
        except Exception as e:
            logger.error(f"❌ 认证失败: {e}")
            return False
    
    def get_tech_universe(self) -> List[str]:
        """获取科技主线股票池"""
        # 中证科技100 + 创业板指成分股
        stocks = []
        
        try:
            # 创业板
            stocks += jq.get_index_stocks('399006.XSHE')[:50]
            # 科创50
            stocks += jq.get_index_stocks('000688.XSHG')[:30] if jq.get_index_stocks('000688.XSHG') else []
            # 中证500中的科技股 (通过行业筛选)
            zz500 = jq.get_index_stocks('000905.XSHG')
            
            # 筛选科技行业
            for stock in zz500[:100]:
                try:
                    info = jq.get_security_info(stock)
                    if info and any(kw in info.display_name for kw in TECH_KEYWORDS):
                        stocks.append(stock)
                except:
                    continue
        except:
            pass
        
        return list(set(stocks))
    
    def fetch_stock_data(self, stock: str, date: str) -> Dict:
        """获取股票数据"""
        data = {'symbol': stock}
        
        try:
            # 基本信息
            info = jq.get_security_info(stock)
            if info:
                data['name'] = info.display_name
            
            # 基本面数据
            q = jq.query(
                jq.valuation.code,
                jq.valuation.pe_ratio,
                jq.valuation.pb_ratio,
                jq.valuation.market_cap,
                jq.indicator.roe,
                jq.indicator.roa,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
                jq.indicator.gross_profit_margin
            ).filter(jq.valuation.code == stock)
            
            fund_df = jq.get_fundamentals(q, date=date)
            
            if not fund_df.empty:
                data['pe'] = fund_df['pe_ratio'].iloc[0] or 50
                data['pb'] = fund_df['pb_ratio'].iloc[0] or 3
                data['market_cap'] = (fund_df['market_cap'].iloc[0] or 100) / 100000000  # 转亿
                data['roe'] = fund_df['roe'].iloc[0] or 0
                data['roa'] = fund_df['roa'].iloc[0] or 0
                data['revenue_growth'] = fund_df['inc_revenue_year_on_year'].iloc[0] or 0
                data['profit_growth'] = fund_df['inc_net_profit_year_on_year'].iloc[0] or 0
                data['gross_margin'] = fund_df['gross_profit_margin'].iloc[0] or 0
            
            # 技术数据
            price_df = jq.get_price(
                stock, end_date=date, count=60,
                frequency='daily', fields=['close', 'volume']
            )
            
            if price_df is not None and len(price_df) >= 60:
                close = price_df['close'].values
                volume = price_df['volume'].values
                
                data['momentum_5d'] = (close[-1] / close[-5] - 1) * 100 if close[-5] > 0 else 0
                data['momentum_20d'] = (close[-1] / close[-20] - 1) * 100 if close[-20] > 0 else 0
                data['momentum_60d'] = (close[-1] / close[0] - 1) * 100 if close[0] > 0 else 0
                data['vol_ratio'] = np.mean(volume[-5:]) / np.mean(volume[-20:]) if np.mean(volume[-20:]) > 0 else 1
                data['current_price'] = close[-1]
            
            # 行业
            try:
                ind = jq.get_industry(stock, date=date)
                if ind and stock in ind:
                    data['industry'] = ind[stock].get('sw_l1', {}).get('industry_name', '')
            except:
                data['industry'] = ''
            
        except Exception as e:
            logger.warning(f"获取{stock}数据失败: {e}")
        
        return data
    
    def scan_and_score(self, date: str = None) -> List[Dict]:
        """扫描并打分"""
        if not self.authenticate_jqdata():
            return []
        
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        logger.info(f"📊 开始扫描 ({date})...")
        
        # 获取股票池
        universe = self.get_tech_universe()
        logger.info(f"   股票池: {len(universe)}只")
        
        # 扫描并打分
        results = []
        for i, stock in enumerate(universe):
            if i % 20 == 0:
                logger.info(f"   进度: {i}/{len(universe)}")
            
            data = self.fetch_stock_data(stock, date)
            if data.get('name'):
                score_result = self.scorer.score(stock, data.get('name', ''), data)
                score_result['data'] = data
                results.append(score_result)
        
        # 按得分排序
        results.sort(key=lambda x: x['total_score'], reverse=True)
        
        logger.info(f"✅ 扫描完成: {len(results)}只股票")
        
        return results
    
    def get_top_candidates(self, results: List[Dict], top_n: int = 5) -> List[Dict]:
        """获取Top候选"""
        # 只保留S1-S3阶段的高分股票
        filtered = [
            r for r in results
            if r['total_score'] >= 70 and r.get('stage', 'S0') in ['S1', 'S2', 'S3']
        ]
        
        return filtered[:top_n]
    
    def run_backtest(self, start_date: str, end_date: str, initial_capital: float = 1000000) -> Dict:
        """运行回测"""
        if not self.authenticate_jqdata():
            return {'success': False, 'error': 'JQData认证失败'}
        
        logger.info(f"🚀 开始回测: {start_date} ~ {end_date}")
        
        # 获取交易日
        trade_days = jq.get_trade_days(start_date=start_date, end_date=end_date)
        trade_days = [str(d) for d in trade_days]
        
        # 获取股票池
        universe = self.get_tech_universe()[:50]  # 限制数量
        
        # 预加载价格数据
        logger.info("   预加载价格数据...")
        price_df = jq.get_price(
            universe,
            start_date=start_date,
            end_date=end_date,
            frequency='daily',
            fields=['close'],
            panel=False,
            skip_paused=True
        )
        
        price_cache = {}
        if price_df is not None:
            for stock in universe:
                sdf = price_df[price_df['code'] == stock].copy()
                if not sdf.empty:
                    sdf.set_index('time', inplace=True)
                    price_cache[stock] = sdf
        
        # 初始化
        cash = initial_capital
        positions = {}
        equity_curve = [cash]
        trades = []
        
        rebalance_days = self.config.get('rebalance_days', 10)
        counter = 0
        
        for i, date in enumerate(trade_days):
            if i % 50 == 0:
                logger.info(f"   进度: {i}/{len(trade_days)} ({date})")
            
            # 更新持仓价值和最高价
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    current_price = price_cache[stock].loc[date, 'close']
                    pos['current_price'] = current_price
                    pos['highest_price'] = max(pos.get('highest_price', current_price), current_price)
                    portfolio_value += pos['shares'] * current_price
            
            # 调仓检查
            counter += 1
            if counter >= rebalance_days:
                counter = 0
                
                # 简化版: 基于动量和价格位置打分
                scores = {}
                for stock in universe:
                    if stock in price_cache:
                        try:
                            sdf = price_cache[stock]
                            mask = sdf.index <= date
                            sdf = sdf[mask].tail(60)
                            
                            if len(sdf) >= 60:
                                close = sdf['close'].values
                                
                                momentum_20d = (close[-1] / close[-20] - 1) * 100
                                momentum_60d = (close[-1] / close[0] - 1) * 100
                                price_to_ma20 = (close[-1] / np.mean(close[-20:]) - 1) * 100
                                
                                # 简化打分
                                score = 50 + momentum_20d * 0.5 + momentum_60d * 0.3
                                if price_to_ma20 > 0:
                                    score += 10
                                
                                if score >= self.swing_engine.min_score:
                                    scores[stock] = score
                        except:
                            continue
                
                candidates = [
                    {'symbol': s, 'total_score': sc, 'stage': 'S2', 'name': ''}
                    for s, sc in sorted(scores.items(), key=lambda x: x[1], reverse=True)
                ]
                
                # 生成交易信号
                signals = self.swing_engine.generate_signals(candidates, positions)
                
                # 执行交易
                for signal in signals:
                    stock = signal['symbol']
                    
                    if signal['action'] == 'SELL' and stock in positions:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            value = positions[stock]['shares'] * price * 0.9985  # 扣费
                            cash += value
                            trades.append({
                                'date': date,
                                'symbol': stock,
                                'action': 'SELL',
                                'price': price,
                                'shares': positions[stock]['shares'],
                                'reason': signal['reason']
                            })
                            del positions[stock]
                    
                    elif signal['action'] == 'BUY' and stock not in positions:
                        if stock in price_cache and date in price_cache[stock].index:
                            price = price_cache[stock].loc[date, 'close']
                            target_value = portfolio_value / self.swing_engine.max_holdings
                            buy_value = min(target_value, cash)
                            shares = int(buy_value / price / 100) * 100
                            
                            if shares > 0:
                                cost = shares * price * 1.0003  # 扣费
                                if cost <= cash:
                                    cash -= cost
                                    positions[stock] = {
                                        'shares': shares,
                                        'cost': price,
                                        'highest_price': price,
                                        'current_price': price
                                    }
                                    trades.append({
                                        'date': date,
                                        'symbol': stock,
                                        'action': 'BUY',
                                        'price': price,
                                        'shares': shares,
                                        'reason': signal['reason']
                                    })
            
            # 更新净值
            portfolio_value = cash
            for stock, pos in positions.items():
                if stock in price_cache and date in price_cache[stock].index:
                    portfolio_value += pos['shares'] * price_cache[stock].loc[date, 'close']
            
            equity_curve.append(portfolio_value)
        
        # 计算指标
        equity = pd.Series(equity_curve)
        returns = equity.pct_change().fillna(0)
        
        total_return = (equity.iloc[-1] / initial_capital) - 1
        days = len(equity)
        annual_return = (1 + total_return) ** (252 / days) - 1 if days > 1 else 0
        volatility = returns.std() * np.sqrt(252)
        sharpe = annual_return / volatility if volatility > 0 else 0
        
        peak = equity.cummax()
        drawdown = (equity - peak) / peak
        max_dd = abs(drawdown.min())
        
        calmar = annual_return / max_dd if max_dd > 0 else 0
        
        logger.info(f"✅ 回测完成")
        logger.info(f"   总收益: {total_return*100:.2f}%")
        logger.info(f"   年化收益: {annual_return*100:.2f}%")
        logger.info(f"   夏普比率: {sharpe:.2f}")
        logger.info(f"   最大回撤: {max_dd*100:.2f}%")
        
        return {
            'success': True,
            'metrics': {
                'total_return': total_return,
                'annual_return': annual_return,
                'sharpe_ratio': sharpe,
                'calmar_ratio': calmar,
                'max_drawdown': max_dd,
                'volatility': volatility
            },
            'equity_curve': equity_curve,
            'trades': trades,
            'trade_count': len(trades)
        }
    
    def generate_report(self, scan_results: List[Dict], backtest_results: Dict) -> str:
        """生成HTML报告"""
        metrics = backtest_results.get('metrics', {})
        top_candidates = self.get_top_candidates(scan_results, 5)
        
        # 生成图表
        chart_html = ""
        if MATPLOTLIB_AVAILABLE and backtest_results.get('equity_curve'):
            fig, axes = plt.subplots(1, 2, figsize=(14, 5))
            
            equity = backtest_results['equity_curve']
            axes[0].plot(equity, linewidth=2, color='#667eea')
            axes[0].fill_between(range(len(equity)), equity[0], equity, alpha=0.3, color='#667eea')
            axes[0].set_title('Portfolio Value', fontweight='bold')
            axes[0].grid(True, alpha=0.3)
            
            # 回撤
            equity_s = pd.Series(equity)
            peak = equity_s.cummax()
            dd = (equity_s - peak) / peak
            axes[1].fill_between(range(len(dd)), 0, dd * 100, color='#f87171', alpha=0.6)
            axes[1].set_title('Drawdown (%)', fontweight='bold')
            axes[1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            buf = BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            buf.seek(0)
            chart_b64 = base64.b64encode(buf.read()).decode()
            plt.close(fig)
            
            chart_html = f'<img src="data:image/png;base64,{chart_b64}" style="max-width:100%;">'
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>十倍股多因子量化系统报告</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e0e0e0; padding: 30px; margin: 0; min-height: 100vh; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea, #764ba2); padding: 50px; border-radius: 24px; margin-bottom: 40px; text-align: center; box-shadow: 0 20px 60px rgba(102,126,234,0.3); }}
        .header h1 {{ font-size: 2.8em; margin: 0 0 15px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }}
        .header p {{ margin: 8px 0; opacity: 0.9; font-size: 1.1em; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 25px; margin: 40px 0; }}
        .metric {{ background: rgba(255,255,255,0.08); padding: 30px; border-radius: 20px; text-align: center; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.1); }}
        .metric .label {{ color: #aaa; font-size: 0.9em; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }}
        .metric .value {{ font-size: 2.5em; font-weight: 700; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .metric .value.positive {{ background: linear-gradient(135deg, #4ade80, #22c55e); -webkit-background-clip: text; }}
        .metric .value.negative {{ background: linear-gradient(135deg, #f87171, #ef4444); -webkit-background-clip: text; }}
        .section {{ background: rgba(255,255,255,0.05); padding: 35px; border-radius: 24px; margin-bottom: 35px; backdrop-filter: blur(10px); }}
        .section h2 {{ color: #667eea; margin-top: 0; font-size: 1.6em; border-bottom: 2px solid rgba(102,126,234,0.3); padding-bottom: 15px; }}
        .chart {{ text-align: center; margin: 25px 0; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        th {{ background: rgba(102,126,234,0.2); font-weight: 600; }}
        tr:hover {{ background: rgba(102,126,234,0.1); }}
        .tag {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 0.85em; margin: 3px; }}
        .tag-s {{ background: linear-gradient(135deg, #4ade80, #22c55e); color: white; }}
        .tag-a {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
        .tag-stage {{ background: rgba(251,191,36,0.2); color: #fbbf24; }}
        .highlight {{ color: #4ade80; font-weight: bold; }}
        .stock-card {{ background: rgba(255,255,255,0.05); border-radius: 16px; padding: 25px; margin: 15px 0; border-left: 4px solid #667eea; }}
        .stock-card h3 {{ margin: 0 0 15px 0; color: #667eea; }}
        .signals {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 十倍股多因子量化系统</h1>
            <p>整合阶段识别 | 7维评分卡 | 多因子打分 | 科技主线聚焦</p>
            <p>目标：聚焦5只以内股票，波段操作，控制回撤</p>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="label">总收益率</div>
                <div class="value {'positive' if metrics.get('total_return', 0) > 0 else 'negative'}">{metrics.get('total_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">年化收益</div>
                <div class="value {'positive' if metrics.get('annual_return', 0) > 0 else 'negative'}">{metrics.get('annual_return', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">夏普比率</div>
                <div class="value">{metrics.get('sharpe_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">卡玛比率</div>
                <div class="value">{metrics.get('calmar_ratio', 0):.2f}</div>
            </div>
            <div class="metric">
                <div class="label">最大回撤</div>
                <div class="value negative">{metrics.get('max_drawdown', 0)*100:.2f}%</div>
            </div>
            <div class="metric">
                <div class="label">交易次数</div>
                <div class="value">{backtest_results.get('trade_count', 0)}</div>
            </div>
        </div>
        
        <div class="section">
            <h2>📊 回测图表</h2>
            <div class="chart">{chart_html}</div>
        </div>
        
        <div class="section">
            <h2>🎯 Top 5 候选股票</h2>
            {''.join([f'''
            <div class="stock-card">
                <h3>{c.get('name', '')} ({c.get('symbol', '')})</h3>
                <p><span class="tag tag-{'s' if c.get('scorecard_grade','C') in ['S+','S'] else 'a'}">评分: {c.get('total_score', 0):.1f}</span>
                   <span class="tag tag-stage">阶段: {c.get('stage', 'S0')}</span>
                   <span class="tag">推荐: {c.get('recommendation', '')}</span></p>
                <div class="signals">
                    {''.join([f'<span class="tag" style="background:rgba(74,222,128,0.2);color:#4ade80">{s}</span>' for s in c.get('stage_signals', [])[:3]])}
                    {''.join([f'<span class="tag" style="background:rgba(102,126,234,0.2);color:#667eea">{s}</span>' for s in c.get('scorecard_signals', [])[:3]])}
                </div>
            </div>
            ''' for c in top_candidates])}
        </div>
        
        <div class="section">
            <h2>📋 系统说明</h2>
            <table>
                <tr><th>模块</th><th>说明</th></tr>
                <tr><td>阶段识别</td><td>S0(观察)→S1(验证)→S2(导入,最佳买点)→S3(放量)→S4(加速)→S5(成熟)</td></tr>
                <tr><td>7维评分卡</td><td>盈利能力/成长性/财务健康/估值水平/行业地位/管理质量/市场表现</td></tr>
                <tr><td>多因子打分</td><td>基本面(40%)+估值(15%)+技术(25%)+阶段(20%)</td></tr>
                <tr><td>科技主线</td><td>AI/半导体/新能源/量子计算/生物医药</td></tr>
                <tr><td>波段操作</td><td>止损{self.swing_engine.stop_loss*100:.0f}%/止盈{self.swing_engine.take_profit*100:.0f}%/移动止损{self.swing_engine.trailing_stop*100:.0f}%</td></tr>
            </table>
        </div>
    </div>
</body>
</html>"""
        
        return html


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    logger.info("=" * 80)
    logger.info("🚀 十倍股多因子量化系统")
    logger.info("=" * 80)
    
    # 配置
    config = {
        'jqdata_username': '13327806797',
        'max_holdings': 5,
        'stop_loss': -0.10,
        'take_profit': 0.50,
        'trailing_stop': 0.15,
        'min_score': 65,
        'rebalance_days': 10,
    }
    
    # 创建系统
    system = TenbaggerMultifactorSystem(config)
    
    # 1. 扫描并打分
    scan_date = datetime.now().strftime('%Y-%m-%d')
    scan_results = system.scan_and_score(scan_date)
    
    # 2. 回测
    backtest_results = system.run_backtest(
        start_date="2024-01-01",
        end_date="2025-12-20",
        initial_capital=1000000
    )
    
    # 3. 生成报告
    logger.info("📝 生成报告...")
    html = system.generate_report(scan_results, backtest_results)
    
    # 保存报告
    reports_dir = PROJECT_ROOT / "research" / "tenbagger_10x_strategy" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = reports_dir / f"tenbagger_multifactor_system_{timestamp}.html"
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    logger.info(f"✅ 报告已保存: {report_path}")
    
    # 登出
    jq.logout()
    
    # 打印Top候选
    logger.info("\n🎯 Top 5 候选股票:")
    for c in system.get_top_candidates(scan_results, 5):
        logger.info(f"   {c['name']} ({c['symbol']}): 得分 {c['total_score']:.1f}, 阶段 {c['stage']}")
    
    logger.info("=" * 80)
    
    return {
        'scan_results': scan_results,
        'backtest_results': backtest_results,
        'report_path': str(report_path)
    }


if __name__ == "__main__":
    main()









































