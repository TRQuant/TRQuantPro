#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
本周投资推荐系统 v2.0
====================

三维度综合推荐：
1. 基本面维度：十倍股筛选（放宽条件）- 数据来源：JQData
2. 技术面维度：动量信号、趋势确认 - 数据来源：AKShare（实时）+ JQData（历史）
3. 催化剂维度：行业热点、事件驱动 - 数据来源：AKShare

输出：
- 投资标的列表（按综合得分排序）
- 交易策略（买入时机、止盈止损）
- 仓位建议（根据市场环境）

数据来源说明：
- JQData: 基本面数据（财务指标、估值）、历史行情
- AKShare: 当日实时行情、行业涨跌、北向资金等
"""

import sys
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import warnings
warnings.filterwarnings('ignore')

PROJECT_ROOT = '/home/taotao/.cursor/worktrees/TRQuant/ope'
sys.path.insert(0, PROJECT_ROOT)

import pandas as pd
import numpy as np
import jqdatasdk as jq
from jqdata.auth import authenticate

# AKShare用于实时数据
try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    print("⚠️ AKShare未安装，将仅使用JQData")


# ============================================================
# 配置参数
# ============================================================

# 基本面筛选条件（极度放宽版 - 应对数据滞后）
FUNDAMENTAL_CONFIG = {
    'min_mcap': 10,           # 最小市值（亿）
    'max_mcap': 3000,         # 最大市值（亿）
    'min_profit_growth': -0.20,# 利润增速（允许微跌，看趋势）
    'min_revenue_growth': -0.10,# 营收增速（允许微跌）
    'min_roe': 0.05,          # 最小ROE（5%）
    'max_pe': 300,            # 最大PE（允许高成长股）
}

# 动量评分权重
MOMENTUM_WEIGHTS = {
    'mom_5d': 0.15,           # 5日动量
    'mom_20d': 0.20,          # 20日动量
    'price_pos': 0.15,        # 区间位置
    'ma_align': 0.20,         # 均线排列
    'vol_ratio': 0.10,        # 量比
    'rsi': 0.10,              # RSI
    'trend': 0.10,            # 趋势强度
}

# 行业热点（当前关注的行业）
HOT_INDUSTRIES = [
    'AI人工智能', '半导体', '新能源', '消费电子', 
    '汽车', '医药生物', '食品饮料', '计算机'
]

# 申万一级行业映射到热点
INDUSTRY_HOTSPOT_MAP = {
    '电子': ['半导体', '消费电子', 'AI人工智能'],
    '计算机': ['AI人工智能', '云计算'],
    '通信': ['5G', 'AI人工智能'],
    '电气设备': ['新能源', '储能'],
    '汽车': ['新能源车', '智能驾驶'],
    '医药生物': ['创新药', '医疗器械'],
    '食品饮料': ['消费升级'],
    '家用电器': ['智能家居', '消费电子'],
    '机械设备': ['高端制造', '机器人'],
}

# 排除行业
EXCLUDE_INDUSTRIES = ['有色金属', '钢铁', '采掘', '农林牧渔', '房地产']


# ============================================================
# AKShare 实时数据获取
# ============================================================

def get_realtime_market_data() -> Dict:
    """
    【步骤1】获取当日实时市场数据 (AKShare)
    
    逻辑说明：
    - 使用AKShare获取A股实时行情
    - 包含当日涨跌幅、成交量、换手率等
    - 补充JQData的T+1延迟
    """
    if not AKSHARE_AVAILABLE:
        return {}
    
    print("\n  📡 [AKShare] 获取当日实时行情...")
    
    try:
        # 获取A股实时行情
        df = ak.stock_zh_a_spot_em()
        
        if df is not None and not df.empty:
            # 重命名列
            df = df.rename(columns={
                '代码': 'code',
                '名称': 'name', 
                '最新价': 'price',
                '涨跌幅': 'change_pct',
                '涨跌额': 'change',
                '成交量': 'volume',
                '成交额': 'amount',
                '振幅': 'amplitude',
                '换手率': 'turnover',
                '量比': 'vol_ratio',
                '60日涨跌幅': 'change_60d',
                '年初至今涨跌幅': 'change_ytd',
            })
            
            # 转换代码格式
            def convert_code(code):
                if code.startswith('6'):
                    return f"{code}.XSHG"
                elif code.startswith(('0', '3')):
                    return f"{code}.XSHE"
                return code
            
            df['code'] = df['code'].apply(convert_code)
            df = df.set_index('code')
            
            print(f"     获取 {len(df)} 只股票实时数据")
            return df.to_dict('index')
    except Exception as e:
        print(f"     ⚠️ 获取实时数据失败: {e}")
    
    return {}


def get_realtime_index_data() -> Dict:
    """
    【步骤2】获取主要指数实时数据 (AKShare)
    
    逻辑说明：
    - 获取沪深300、上证指数、创业板指等
    - 用于判断当日市场情绪
    """
    if not AKSHARE_AVAILABLE:
        return {}
    
    print("\n  📡 [AKShare] 获取指数实时数据...")
    
    try:
        df = ak.stock_zh_index_spot_em()
        
        indices = {
            '上证指数': None,
            '深证成指': None,
            '创业板指': None,
            '沪深300': None,
        }
        
        for _, row in df.iterrows():
            name = row.get('名称', '')
            if name in indices:
                indices[name] = {
                    'price': row.get('最新价', 0),
                    'change_pct': row.get('涨跌幅', 0),
                }
        
        print(f"     上证: {indices.get('上证指数', {}).get('change_pct', 0):+.2f}%")
        print(f"     创业板: {indices.get('创业板指', {}).get('change_pct', 0):+.2f}%")
        
        return indices
    except Exception as e:
        print(f"     ⚠️ 获取指数数据失败: {e}")
    
    return {}


def get_industry_realtime_performance() -> Dict[str, float]:
    """
    【步骤3】获取行业板块实时涨跌 (AKShare)
    
    逻辑说明：
    - 获取申万一级行业当日涨跌
    - 识别今日热点行业
    - 用于催化剂评分
    """
    if not AKSHARE_AVAILABLE:
        return {}
    
    print("\n  📡 [AKShare] 获取行业板块实时数据...")
    
    try:
        # 申万行业实时数据
        df = ak.stock_board_industry_name_em()
        
        performances = {}
        for _, row in df.iterrows():
            name = row.get('板块名称', '')
            change = row.get('涨跌幅', 0)
            if pd.notna(change):
                performances[name] = float(change)
        
        # 排序显示
        sorted_ind = sorted(performances.items(), key=lambda x: x[1], reverse=True)[:5]
        print("     今日热点行业:")
        for name, change in sorted_ind:
            print(f"       {name}: {change:+.2f}%")
        
        return performances
    except Exception as e:
        print(f"     ⚠️ 获取行业数据失败: {e}")
    
    return {}


def get_north_money_flow() -> Dict:
    """
    【步骤4】获取北向资金流向 (AKShare)
    
    逻辑说明：
    - 北向资金是外资风向标
    - 大幅流入通常是利好信号
    - 用于市场情绪判断
    """
    if not AKSHARE_AVAILABLE:
        return {}
    
    print("\n  📡 [AKShare] 获取北向资金数据...")
    
    try:
        df = ak.stock_hsgt_north_net_flow_in_em()
        
        if df is not None and not df.empty:
            latest = df.iloc[-1]
            flow = latest.get('北向资金', latest.get('当日净流入', 0))
            
            # 转换为亿元
            if abs(flow) > 1e8:
                flow = flow / 1e8
            
            print(f"     今日北向资金: {flow:+.2f}亿")
            
            return {
                'net_flow': flow,
                'is_positive': flow > 0,
            }
    except Exception as e:
        print(f"     ⚠️ 获取北向资金失败: {e}")
    
    return {}


# ============================================================
# 数据结构
# ============================================================

class MarketRegime(Enum):
    BULL = "牛市"
    BEAR = "熊市"
    VOLATILE = "震荡"


@dataclass
class StockScore:
    """股票综合评分"""
    code: str
    name: str
    industry: str
    
    # 基本面
    market_cap: float
    pe: float
    roe: float
    profit_growth: float
    revenue_growth: float
    fundamental_score: float = 0
    
    # 动量
    mom_5d: float = 0
    mom_20d: float = 0
    price_position: float = 0
    ma_aligned: bool = False
    vol_ratio: float = 0
    rsi: float = 0
    momentum_score: float = 0
    
    # 催化剂
    is_hot_industry: bool = False
    catalyst_score: float = 0
    
    # 综合
    total_score: float = 0
    
    # 策略
    buy_price: float = 0
    stop_loss: float = 0
    take_profit: float = 0
    strategy: str = ""


@dataclass
class MarketAnalysis:
    """市场分析结果"""
    regime: MarketRegime
    index_price: float
    ma20: float
    ma60: float
    change_5d: float
    change_20d: float
    rsi: float
    position_advice: float
    risk_level: str
    summary: str


# ============================================================
# 市场环境分析
# ============================================================

def analyze_market() -> MarketAnalysis:
    """分析当前市场环境"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d')
    
    price = jq.get_price(
        '000300.XSHG',
        start_date=start_date,
        end_date=end_date,
        frequency='daily',
        fields=['close', 'volume'],
        panel=False
    )
    
    if price is None or len(price) < 60:
        return MarketAnalysis(
            regime=MarketRegime.VOLATILE,
            index_price=0, ma20=0, ma60=0,
            change_5d=0, change_20d=0, rsi=50,
            position_advice=0.5, risk_level="中等",
            summary="数据不足，建议谨慎"
        )
    
    close = price['close']
    current = close.iloc[-1]
    ma20 = close.rolling(20).mean().iloc[-1]
    ma60 = close.rolling(60).mean().iloc[-1]
    
    change_5d = (current - close.iloc[-6]) / close.iloc[-6] * 100 if len(close) > 5 else 0
    change_20d = (current - close.iloc[-21]) / close.iloc[-21] * 100 if len(close) > 20 else 0
    
    # RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi = 100 - (100 / (1 + gain.iloc[-1] / (loss.iloc[-1] + 0.0001)))
    
    # 判断市场环境
    if current > ma20 > ma60 and change_20d > 0:
        regime = MarketRegime.BULL
        position_advice = 0.8
        risk_level = "低"
        summary = f"牛市格局，指数站上均线，20日涨幅{change_20d:.1f}%"
    elif current < ma20 < ma60 and change_20d < 0:
        regime = MarketRegime.BEAR
        position_advice = 0.2
        risk_level = "高"
        summary = f"熊市格局，指数跌破均线，20日跌幅{change_20d:.1f}%"
    else:
        regime = MarketRegime.VOLATILE
        position_advice = 0.5
        risk_level = "中等"
        summary = f"震荡市，方向不明，建议精选个股"
    
    return MarketAnalysis(
        regime=regime,
        index_price=current,
        ma20=ma20,
        ma60=ma60,
        change_5d=change_5d,
        change_20d=change_20d,
        rsi=rsi,
        position_advice=position_advice,
        risk_level=risk_level,
        summary=summary
    )


# ============================================================
# 行业热点分析
# ============================================================

def analyze_industry_performance() -> Dict[str, float]:
    """分析行业近期表现 - 使用行业龙头ETF或指数"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    # 使用行业ETF代替指数（更容易获取）
    industry_etfs = {
        '电子': '512480.XSHG',      # 半导体ETF
        '计算机': '512720.XSHG',    # 计算机ETF
        '通信': '515880.XSHG',      # 通信ETF
        '新能源': '516160.XSHG',    # 新能源ETF
        '汽车': '516110.XSHG',      # 汽车ETF
        '医药': '512010.XSHG',      # 医药ETF
        '消费': '159928.XSHE',      # 消费ETF
        '银行': '512800.XSHG',      # 银行ETF
        '证券': '512880.XSHG',      # 证券ETF
        '军工': '512660.XSHG',      # 军工ETF
    }
    
    performances = {}
    
    for name, code in industry_etfs.items():
        try:
            price = jq.get_price(
                code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['close'],
                panel=False
            )
            if price is not None and len(price) > 5:
                ret = (price['close'].iloc[-1] - price['close'].iloc[0]) / price['close'].iloc[0] * 100
                performances[name] = ret
        except:
            performances[name] = 0
    
    return performances


# ============================================================
# 数据获取
# ============================================================

def get_stock_universe(date_str: str) -> pd.DataFrame:
    """获取股票池"""
    all_stocks = jq.get_all_securities(types=['stock'], date=date_str)
    
    # 基础过滤
    valid = all_stocks[
        ~all_stocks['display_name'].str.contains('ST|退', na=False) &
        ~all_stocks.index.str.startswith('688') &  # 科创板
        ~all_stocks.index.str.startswith('8')      # 北交所
    ]
    
    # 获取行业
    codes = valid.index.tolist()
    industries = jq.get_industry(codes, date=date_str)
    
    valid = valid.copy()
    valid['industry'] = ''
    for code in codes:
        if code in industries and 'sw_l1' in industries[code]:
            valid.loc[code, 'industry'] = industries[code]['sw_l1'].get('industry_name', '')
    
    return valid


def get_fundamentals_data(codes: List[str], date_str: str) -> pd.DataFrame:
    """获取基本面数据"""
    batch_size = 500
    all_data = []
    
    for i in range(0, len(codes), batch_size):
        batch = codes[i:i+batch_size]
        
        try:
            # 估值数据
            q_val = jq.query(
                jq.valuation.code,
                jq.valuation.market_cap,
                jq.valuation.pe_ratio,
            ).filter(jq.valuation.code.in_(batch))
            df_val = jq.get_fundamentals(q_val, date=date_str)
            
            # 指标数据
            q_ind = jq.query(
                jq.indicator.code,
                jq.indicator.roe,
                jq.indicator.inc_revenue_year_on_year,
                jq.indicator.inc_net_profit_year_on_year,
            ).filter(jq.indicator.code.in_(batch))
            df_ind = jq.get_fundamentals(q_ind, date=date_str)
            
            if df_val is not None and df_ind is not None and not df_val.empty and not df_ind.empty:
                df_merged = df_val.merge(df_ind, on='code', how='inner')
                all_data.append(df_merged)
        except Exception as e:
            continue
    
    if all_data:
        return pd.concat(all_data, ignore_index=True).set_index('code')
    return pd.DataFrame()


def get_price_data(codes: List[str], days: int = 60) -> Dict[str, pd.DataFrame]:
    """获取价格数据"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days+30)).strftime('%Y-%m-%d')
    
    price_data = {}
    
    for code in codes:
        try:
            price = jq.get_price(
                code,
                start_date=start_date,
                end_date=end_date,
                frequency='daily',
                fields=['close', 'volume', 'high', 'low'],
                panel=False
            )
            if price is not None and len(price) >= 20:
                price_data[code] = price
        except:
            continue
    
    return price_data


# ============================================================
# 评分系统
# ============================================================

def calculate_fundamental_score(fund_data: dict) -> float:
    """计算基本面得分"""
    score = 0
    
    # 利润增速 (30分)
    pg = fund_data.get('profit_growth', 0)
    if pg >= 0.50:
        score += 30
    elif pg >= 0.30:
        score += 25
    elif pg >= 0.20:
        score += 20
    elif pg >= 0.10:
        score += 15
    else:
        score += 5
    
    # 营收增速 (20分)
    rg = fund_data.get('revenue_growth', 0)
    if rg >= 0.30:
        score += 20
    elif rg >= 0.20:
        score += 15
    elif rg >= 0.10:
        score += 10
    else:
        score += 5
    
    # ROE (20分)
    roe = fund_data.get('roe', 0)
    if roe >= 0.20:
        score += 20
    elif roe >= 0.15:
        score += 15
    elif roe >= 0.10:
        score += 10
    else:
        score += 5
    
    # 市值 (15分) - 偏好中小市值
    mcap = fund_data.get('market_cap', 0)
    if 30 <= mcap <= 150:
        score += 15  # 最佳区间
    elif 20 <= mcap <= 300:
        score += 10
    elif mcap <= 500:
        score += 5
    
    # PE合理性 (15分)
    pe = fund_data.get('pe', 0)
    if 10 <= pe <= 30:
        score += 15
    elif 30 < pe <= 50:
        score += 10
    elif 50 < pe <= 80:
        score += 5
    
    return score


def calculate_momentum_score(price_df: pd.DataFrame) -> Tuple[float, dict]:
    """计算动量得分"""
    if price_df is None or len(price_df) < 20:
        return 0, {}
    
    close = price_df['close']
    volume = price_df['volume']
    
    # 动量指标
    mom_5d = (close.iloc[-1] - close.iloc[-6]) / close.iloc[-6] * 100 if len(close) > 5 else 0
    mom_20d = (close.iloc[-1] - close.iloc[-21]) / close.iloc[-21] * 100 if len(close) > 20 else 0
    
    # 区间位置 (0-100)
    high_60d = close.rolling(60, min_periods=20).max().iloc[-1]
    low_60d = close.rolling(60, min_periods=20).min().iloc[-1]
    price_pos = (close.iloc[-1] - low_60d) / (high_60d - low_60d + 0.01) * 100
    
    # 均线排列
    ma5 = close.rolling(5).mean().iloc[-1]
    ma10 = close.rolling(10).mean().iloc[-1]
    ma20 = close.rolling(20).mean().iloc[-1]
    ma_aligned = close.iloc[-1] > ma5 > ma10 > ma20
    
    # 量比
    vol_ratio = volume.iloc[-1] / volume.rolling(20).mean().iloc[-1] if volume.rolling(20).mean().iloc[-1] > 0 else 1
    
    # RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
    rsi = 100 - (100 / (1 + gain.iloc[-1] / (loss.iloc[-1] + 0.0001)))
    
    # 计算得分
    score = 0
    
    # 5日动量 (15分)
    if mom_5d > 10:
        score += 15
    elif mom_5d > 5:
        score += 12
    elif mom_5d > 0:
        score += 8
    elif mom_5d > -5:
        score += 5
    
    # 20日动量 (20分)
    if mom_20d > 20:
        score += 20
    elif mom_20d > 10:
        score += 16
    elif mom_20d > 0:
        score += 10
    elif mom_20d > -10:
        score += 5
    
    # 区间位置 (15分)
    if 20 <= price_pos <= 60:  # 回调区间
        score += 15
    elif 60 < price_pos <= 80:
        score += 10
    elif price_pos > 80:
        score += 5  # 高位风险
    else:
        score += 8  # 低位观望
    
    # 均线排列 (20分)
    if ma_aligned:
        score += 20
    elif close.iloc[-1] > ma20:
        score += 10
    
    # 量比 (10分)
    if 1.2 <= vol_ratio <= 2.5:
        score += 10
    elif vol_ratio > 2.5:
        score += 5  # 放量过大
    elif vol_ratio >= 0.8:
        score += 8
    
    # RSI (10分)
    if 40 <= rsi <= 60:
        score += 10
    elif 30 <= rsi <= 70:
        score += 7
    else:
        score += 3
    
    # 趋势强度 (10分)
    if mom_5d > 0 and mom_20d > 0 and ma_aligned:
        score += 10
    elif mom_20d > 0:
        score += 5
    
    details = {
        'mom_5d': mom_5d,
        'mom_20d': mom_20d,
        'price_pos': price_pos,
        'ma_aligned': ma_aligned,
        'vol_ratio': vol_ratio,
        'rsi': rsi,
        'current_price': close.iloc[-1],
        'ma20': ma20,
    }
    
    return score, details


def calculate_catalyst_score(industry: str, industry_perf: Dict[str, float]) -> Tuple[float, bool]:
    """计算催化剂得分"""
    score = 0
    is_hot = False
    
    # 检查是否在排除行业
    if any(exc in industry for exc in EXCLUDE_INDUSTRIES):
        return 0, False
    
    # 行业热点加分
    if industry in INDUSTRY_HOTSPOT_MAP:
        score += 20
        is_hot = True
    
    # 行业近期表现加分
    if industry in industry_perf:
        perf = industry_perf[industry]
        if perf > 10:
            score += 15
        elif perf > 5:
            score += 10
        elif perf > 0:
            score += 5
    
    return score, is_hot


def generate_strategy(stock: StockScore, market: MarketAnalysis) -> str:
    """生成交易策略"""
    strategies = []
    
    # 买入策略
    if stock.momentum_score >= 60 and stock.ma_aligned:
        strategies.append("趋势跟踪：站稳5日线可加仓")
    elif stock.price_position < 50:
        strategies.append("逢低吸纳：回调至20日线附近分批建仓")
    else:
        strategies.append("高位谨慎：等待回调后再介入")
    
    # 止损位
    if stock.ma_aligned:
        stock.stop_loss = stock.buy_price * 0.92  # 8%止损
    else:
        stock.stop_loss = stock.buy_price * 0.90  # 10%止损
    
    # 止盈位
    if market.regime == MarketRegime.BULL:
        stock.take_profit = stock.buy_price * 1.30  # 30%止盈
    else:
        stock.take_profit = stock.buy_price * 1.20  # 20%止盈
    
    return "; ".join(strategies)


# ============================================================
# 主程序
# ============================================================

def get_last_trade_date() -> str:
    """获取最近的交易日（数据已更新的）"""
    # 聚宽数据通常T+1更新，使用前一个交易日
    today = datetime.now()
    
    # 获取交易日历
    trade_days = jq.get_trade_days(end_date=today, count=5)
    
    # 返回倒数第二个交易日（确保数据已更新）
    if len(trade_days) >= 2:
        return str(trade_days[-2])
    return (today - timedelta(days=1)).strftime('%Y-%m-%d')


def run_weekly_advisor():
    """运行本周投资推荐"""
    
    print("="*80)
    print("本周投资推荐系统 v2.0")
    print("="*80)
    print(f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"数据来源: JQData (基本面) + AKShare (实时行情)")
    
    # ==================== 第一步：数据源初始化 ====================
    print("\n" + "="*80)
    print("【第1步】数据源初始化")
    print("="*80)
    print("""
    逻辑说明：
    - JQData: 提供财务基本面数据（利润增速、ROE、市值等）
    - AKShare: 提供当日实时行情（免费，无延迟）
    - 组合使用解决JQData的T+1数据延迟问题
    """)
    
    # 认证JQData
    print("  🔑 认证JQData...")
    authenticate()
    
    # 使用最近已更新数据的交易日（基本面数据）
    date_str = get_last_trade_date()
    print(f"  📅 基本面数据日期: {date_str}")
    
    # ==================== 第二步：获取实时数据 ====================
    print("\n" + "="*80)
    print("【第2步】获取实时市场数据 (AKShare)")
    print("="*80)
    print("""
    逻辑说明：
    - 实时行情用于计算当日动量和情绪
    - 行业板块数据识别今日热点
    - 北向资金判断外资态度
    """)
    
    # AKShare实时数据
    realtime_data = get_realtime_market_data()
    index_data = get_realtime_index_data()
    industry_realtime = get_industry_realtime_performance()
    north_flow = get_north_money_flow()
    
    # ==================== 第三步：市场环境分析 ====================
    print("\n" + "="*80)
    print("【第3步】市场环境分析")
    print("="*80)
    print("""
    逻辑说明：
    - 判断当前是牛市/熊市/震荡
    - 基于均线位置 (价格 vs MA20 vs MA60)
    - 基于趋势动量 (20日涨跌幅)
    - 输出建议仓位比例
    """)
    
    market = analyze_market()
    print(f"\n  📊 市场状态: {market.regime.value}")
    print(f"  沪深300: {market.index_price:.2f}")
    print(f"  MA20: {market.ma20:.2f} | MA60: {market.ma60:.2f}")
    print(f"  5日涨幅: {market.change_5d:.2f}% | 20日涨幅: {market.change_20d:.2f}%")
    print(f"  RSI: {market.rsi:.1f}")
    
    # 结合实时指数数据
    if index_data:
        today_change = index_data.get('沪深300', {}).get('change_pct', 0)
        print(f"  今日涨幅: {today_change:+.2f}% (实时)")
    
    print(f"\n  💡 判断: {market.summary}")
    print(f"  📌 建议仓位: {market.position_advice*100:.0f}%")
    print(f"  ⚠️ 风险等级: {market.risk_level}")
    
    # 北向资金
    if north_flow.get('net_flow'):
        flow = north_flow['net_flow']
        print(f"  💰 北向资金: {flow:+.2f}亿 ({'流入利好' if flow > 0 else '流出谨慎'})")
    
    # ==================== 第四步：行业热点分析 ====================
    print("\n" + "="*80)
    print("【第4步】行业热点分析")
    print("="*80)
    print("""
    逻辑说明：
    - 近30日行业涨幅排名 (JQData ETF)
    - 今日实时行业涨跌 (AKShare)
    - 热点行业股票获得催化剂加分
    """)
    
    industry_perf = analyze_industry_performance()
    sorted_industries = sorted(industry_perf.items(), key=lambda x: x[1], reverse=True)
    
    print("\n  📈 近30日行业涨幅排名 (ETF):")
    for i, (ind, perf) in enumerate(sorted_industries[:5], 1):
        print(f"     {i}. {ind}: {perf:+.2f}%")
    
    # 结合实时行业数据
    if industry_realtime:
        sorted_realtime = sorted(industry_realtime.items(), key=lambda x: x[1], reverse=True)[:5]
        print("\n  🔥 今日热点行业 (实时):")
        for i, (ind, perf) in enumerate(sorted_realtime, 1):
            print(f"     {i}. {ind}: {perf:+.2f}%")
    
    hot_industries_now = [ind for ind, perf in sorted_industries[:5] if perf > 0]
    
    # ==================== 第五步：股票池筛选 ====================
    print("\n" + "="*80)
    print("【第5步】股票池基本面筛选 (JQData)")
    print("="*80)
    print(f"""
    逻辑说明：
    - 排除ST、退市、科创板、北交所
    - 排除周期性行业（有色、钢铁、采掘等）
    - 市值区间: {FUNDAMENTAL_CONFIG['min_mcap']}-{FUNDAMENTAL_CONFIG['max_mcap']}亿
    - 利润增速: >{FUNDAMENTAL_CONFIG['min_profit_growth']*100:.0f}%
    - ROE: >{FUNDAMENTAL_CONFIG['min_roe']*100:.0f}%
    """)
    
    # 获取股票池
    stocks_df = get_stock_universe(date_str)
    print(f"\n  📋 初始股票池: {len(stocks_df)} 只")
    
    # 获取基本面数据
    codes = stocks_df.index.tolist()
    fundamentals = get_fundamentals_data(codes, date_str)
    print(f"  📊 获取基本面数据: {len(fundamentals)} 只")
    
    if fundamentals.empty:
        print("⚠️ 无法获取基本面数据")
        return
    
    # 第一轮筛选：基本面
    candidates = []
    
    for code in fundamentals.index:
        try:
            fund = fundamentals.loc[code]
            industry = stocks_df.loc[code, 'industry'] if code in stocks_df.index else ''
            name = stocks_df.loc[code, 'display_name'] if code in stocks_df.index else code
            
            # 排除行业
            if any(exc in industry for exc in EXCLUDE_INDUSTRIES):
                continue
            
            market_cap = fund.get('market_cap', 0)
            pe = fund.get('pe_ratio', 0) if pd.notna(fund.get('pe_ratio')) else 0
            roe = fund.get('roe', 0) / 100 if pd.notna(fund.get('roe')) else 0
            revenue_growth = fund.get('inc_revenue_year_on_year', 0) / 100 if pd.notna(fund.get('inc_revenue_year_on_year')) else 0
            profit_growth = fund.get('inc_net_profit_year_on_year', 0) / 100 if pd.notna(fund.get('inc_net_profit_year_on_year')) else 0
            
            # 数据有效性
            if pd.isna(market_cap) or market_cap <= 0:
                continue
            
            # 基本面筛选（放宽版）
            if not (FUNDAMENTAL_CONFIG['min_mcap'] <= market_cap <= FUNDAMENTAL_CONFIG['max_mcap']):
                continue
            # 利润增速放宽 - 允许数据为nan或负增长（看其他维度）
            if pd.notna(profit_growth) and profit_growth < FUNDAMENTAL_CONFIG['min_profit_growth']:
                continue
            # 营收增速放宽
            if pd.notna(revenue_growth) and revenue_growth < FUNDAMENTAL_CONFIG['min_revenue_growth']:
                continue
            # ROE可为空时跳过检查
            if pd.notna(roe) and roe < FUNDAMENTAL_CONFIG['min_roe']:
                continue
            # PE允许负数（亏损股）和高PE（成长股）
            if pd.notna(pe) and pe > 0 and pe > FUNDAMENTAL_CONFIG['max_pe']:
                continue
            
            # 计算基本面得分
            fund_score = calculate_fundamental_score({
                'profit_growth': profit_growth,
                'revenue_growth': revenue_growth,
                'roe': roe,
                'market_cap': market_cap,
                'pe': pe
            })
            
            # 催化剂得分
            catalyst_score, is_hot = calculate_catalyst_score(industry, industry_perf)
            
            candidates.append({
                'code': code,
                'name': name,
                'industry': industry,
                'market_cap': market_cap,
                'pe': pe,
                'roe': roe,
                'profit_growth': profit_growth,
                'revenue_growth': revenue_growth,
                'fundamental_score': fund_score,
                'catalyst_score': catalyst_score,
                'is_hot': is_hot,
            })
        except:
            continue
    
    print(f"  ✅ 基本面筛选后: {len(candidates)} 只")
    
    if not candidates:
        print("  ⚠️ 无符合基本面条件的股票")
        return
    
    # ==================== 第六步：动量评分 ====================
    print("\n" + "="*80)
    print("【第6步】技术面动量评分")
    print("="*80)
    print("""
    逻辑说明：
    - 5日动量: 短期趋势强度 (15分)
    - 20日动量: 中期趋势确认 (20分)
    - 区间位置: 60日高低点位置 (15分)
    - 均线排列: 价格>MA5>MA10>MA20 多头排列 (20分)
    - 量比: 成交量放大信号 (10分)
    - RSI: 超买超卖判断 (10分)
    - 趋势强度: 综合趋势 (10分)
    """)
    
    print("\n  📈 获取价格数据计算动量...")
    candidate_codes = [c['code'] for c in candidates]
    price_data = get_price_data(candidate_codes[:200])  # 限制数量
    print(f"  📊 获取 {len(price_data)} 只股票价格数据")
    
    # ==================== 第七步：综合评分 ====================
    print("\n" + "="*80)
    print("【第7步】综合评分计算")
    print("="*80)
    print("""
    评分权重：
    - 基本面得分: 40% (利润增速、ROE、估值等)
    - 动量得分: 40% (趋势强度、均线、量比等)
    - 催化剂得分: 20% (行业热点、事件驱动)
    
    实时数据加成：
    - 今日涨幅>3%: +5分
    - 今日北向资金买入: +3分
    - 今日行业领涨: +5分
    """)
    
    # 计算综合得分
    results = []
    
    for c in candidates:
        if c['code'] not in price_data:
            continue
        
        price_df = price_data[c['code']]
        momentum_score, mom_details = calculate_momentum_score(price_df)
        
        # 基础综合得分 = 基本面40% + 动量40% + 催化剂20%
        total_score = (
            c['fundamental_score'] * 0.40 +
            momentum_score * 0.40 +
            c['catalyst_score'] * 0.20
        )
        
        # 实时数据加成
        if realtime_data and c['code'] in realtime_data:
            rt = realtime_data[c['code']]
            today_change = rt.get('change_pct', 0)
            if pd.notna(today_change):
                if today_change > 5:
                    total_score += 8  # 强势股加分
                elif today_change > 3:
                    total_score += 5
                elif today_change > 0:
                    total_score += 2
            
            # 量比加成
            rt_vol_ratio = rt.get('vol_ratio', 1)
            if pd.notna(rt_vol_ratio) and rt_vol_ratio > 2:
                total_score += 3
        
        # 北向资金加成
        if north_flow.get('is_positive'):
            total_score += 2
        
        stock = StockScore(
            code=c['code'],
            name=c['name'],
            industry=c['industry'],
            market_cap=c['market_cap'],
            pe=c['pe'],
            roe=c['roe'],
            profit_growth=c['profit_growth'],
            revenue_growth=c['revenue_growth'],
            fundamental_score=c['fundamental_score'],
            mom_5d=mom_details.get('mom_5d', 0),
            mom_20d=mom_details.get('mom_20d', 0),
            price_position=mom_details.get('price_pos', 50),
            ma_aligned=mom_details.get('ma_aligned', False),
            vol_ratio=mom_details.get('vol_ratio', 1),
            rsi=mom_details.get('rsi', 50),
            momentum_score=momentum_score,
            is_hot_industry=c['is_hot'],
            catalyst_score=c['catalyst_score'],
            total_score=total_score,
            buy_price=mom_details.get('current_price', 0),
        )
        
        # 生成策略
        stock.strategy = generate_strategy(stock, market)
        
        results.append(stock)
    
    # 按综合得分排序
    results.sort(key=lambda x: x.total_score, reverse=True)
    
    print(f"\n  ✅ 完成评分: {len(results)} 只股票")
    
    # ==================== 第八步：输出推荐 ====================
    print("\n" + "="*80)
    print("【第8步】本周投资推荐")
    print("="*80)
    print("""
    推荐分级：
    - 🌟 重点推荐: 综合得分 ≥ 60
    - 👀 关注池: 综合得分 50-60
    
    交易策略说明：
    - 趋势跟踪: 均线多头排列，站稳5日线可加仓
    - 逢低吸纳: 回调至20日线附近分批建仓
    - 高位谨慎: 等待回调后再介入
    """)
    
    print(f"\n市场环境: {market.regime.value}")
    print(f"建议总仓位: {market.position_advice*100:.0f}%")
    
    # 重点推荐（得分>60）
    top_picks = [r for r in results if r.total_score >= 60]
    
    print(f"\n{'='*60}")
    print(f"🌟 重点推荐（综合得分≥60）: {len(top_picks)} 只")
    print(f"{'='*60}")
    
    for i, s in enumerate(top_picks[:10], 1):
        print(f"\n{i}. {s.code} {s.name}")
        print(f"   行业: {s.industry} {'🔥热点' if s.is_hot_industry else ''}")
        print(f"   综合得分: {s.total_score:.0f} (基本面{s.fundamental_score:.0f}+动量{s.momentum_score:.0f}+催化{s.catalyst_score:.0f})")
        print(f"   市值: {s.market_cap:.0f}亿 | PE: {s.pe:.1f} | ROE: {s.roe*100:.1f}%")
        print(f"   利润增速: +{s.profit_growth*100:.0f}% | 营收增速: +{s.revenue_growth*100:.0f}%")
        print(f"   5日涨幅: {s.mom_5d:+.1f}% | 20日涨幅: {s.mom_20d:+.1f}% | {'均线多头✓' if s.ma_aligned else '均线混乱'}")
        print(f"   区间位置: {s.price_position:.0f}% | RSI: {s.rsi:.0f}")
        
        # 实时数据补充
        if realtime_data and s.code in realtime_data:
            rt = realtime_data[s.code]
            today_chg = rt.get('change_pct', 0)
            today_vol = rt.get('vol_ratio', 1)
            if pd.notna(today_chg):
                print(f"   📡 今日: {today_chg:+.2f}% | 量比: {today_vol:.2f}")
        
        print(f"   📌 策略: {s.strategy}")
        if s.buy_price > 0:
            print(f"   参考价位: 买入{s.buy_price:.2f} | 止损{s.stop_loss:.2f} | 止盈{s.take_profit:.2f}")
    
    # 关注池（得分50-60）
    watch_list = [r for r in results if 50 <= r.total_score < 60]
    
    if watch_list:
        print(f"\n{'='*60}")
        print(f"👀 关注池（综合得分50-60）: {len(watch_list)} 只")
        print(f"{'='*60}")
        
        for i, s in enumerate(watch_list[:10], 1):
            print(f"  {i}. {s.code} {s.name} - {s.industry}, 得分{s.total_score:.0f}, 利润+{s.profit_growth*100:.0f}%")
    
    # 行业分布
    print(f"\n{'='*60}")
    print("📊 推荐股票行业分布")
    print(f"{'='*60}")
    
    from collections import Counter
    industries = [s.industry for s in top_picks if s.industry]
    if industries:
        ind_count = Counter(industries)
        for ind, cnt in ind_count.most_common(5):
            print(f"  {ind}: {cnt} 只")
    
    # ==================== 风险提示 ====================
    print(f"\n{'='*60}")
    print("⚠️ 风险提示")
    print(f"{'='*60}")
    
    if market.regime == MarketRegime.BEAR:
        print("  - 当前处于熊市环境，建议轻仓操作或观望")
        print("  - 即使有推荐标的，也建议等待市场企稳再介入")
    elif market.regime == MarketRegime.VOLATILE:
        print("  - 当前市场震荡，建议分批建仓，控制单只仓位")
        print("  - 优先选择动量强势且基本面优秀的标的")
    else:
        print("  - 牛市环境可积极配置，但注意止盈纪律")
        print("  - 高位股票需警惕追高风险")
    
    print("  - 本推荐仅供参考，投资有风险，入市需谨慎")
    print("  - 建议结合个人风险偏好和资金情况综合决策")
    
    # 保存结果
    if results:
        df = pd.DataFrame([{
            'code': s.code, 'name': s.name, 'industry': s.industry,
            'total_score': s.total_score,
            'fundamental_score': s.fundamental_score,
            'momentum_score': s.momentum_score,
            'catalyst_score': s.catalyst_score,
            'market_cap': s.market_cap, 'pe': s.pe, 'roe': s.roe,
            'profit_growth': s.profit_growth, 'revenue_growth': s.revenue_growth,
            'mom_5d': s.mom_5d, 'mom_20d': s.mom_20d,
            'price_position': s.price_position, 'ma_aligned': s.ma_aligned,
            'is_hot_industry': s.is_hot_industry,
            'buy_price': s.buy_price, 'stop_loss': s.stop_loss, 'take_profit': s.take_profit,
            'strategy': s.strategy
        } for s in results])
        
        timestamp = datetime.now().strftime('%Y%m%d')
        output = f'{PROJECT_ROOT}/results/weekly_recommendation_{timestamp}.csv'
        df.to_csv(output, index=False, encoding='utf-8-sig')
        print(f"\n详细结果已保存: {output}")
    
    return results, market


if __name__ == '__main__':
    run_weekly_advisor()
