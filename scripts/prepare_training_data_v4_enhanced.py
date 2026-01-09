#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
V4.0增强训练数据准备

从JQData提取完整特征，确保数据质量
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def init_jqdata():
    """初始化JQData"""
    try:
        from config.config_manager import get_config_manager
        import jqdatasdk as jq
        
        cm = get_config_manager()
        jq_config = cm.get_config('jqdata')
        jq.auth(jq_config['username'], jq_config['password'])
        
        logger.info("JQData已连接")
        return jq
    except Exception as e:
        logger.error(f"JQData连接失败: {e}")
        return None


def calculate_technical_indicators(jq, code: str, date: str, lookback: int = 60):
    """计算技术指标"""
    try:
        end_date = pd.to_datetime(date)
        start_date = end_date - timedelta(days=lookback * 2)
        
        df = jq.get_price(
            code,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=date,
            frequency='daily',
            fields=['open', 'high', 'low', 'close', 'volume', 'money'],
            skip_paused=False,
            fq='post'
        )
        
        if df is None or len(df) < 20:
            return {}
        
        close = df['close']
        high = df['high']
        low = df['low']
        volume = df['volume']
        
        indicators = {}
        
        # 动量指标
        indicators['momentum_5d'] = (close.iloc[-1] / close.iloc[-6] - 1) * 100 if len(close) >= 6 else 0
        indicators['momentum_10d'] = (close.iloc[-1] / close.iloc[-11] - 1) * 100 if len(close) >= 11 else 0
        indicators['momentum_20d'] = (close.iloc[-1] / close.iloc[-21] - 1) * 100 if len(close) >= 21 else 0
        
        # RSI
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-10)
        rsi = 100 - (100 / (1 + rs))
        indicators['rsi'] = rsi.iloc[-1] if not pd.isna(rsi.iloc[-1]) else 50
        
        # 相对强度 (vs 20日均值)
        ma20 = close.rolling(window=20).mean()
        indicators['rel_strength'] = (close.iloc[-1] / ma20.iloc[-1] - 1) * 100 if ma20.iloc[-1] > 0 else 0
        
        # 成交量比率
        vol_ma5 = volume.rolling(window=5).mean()
        vol_ma20 = volume.rolling(window=20).mean()
        indicators['volume_ratio'] = vol_ma5.iloc[-1] / vol_ma20.iloc[-1] if vol_ma20.iloc[-1] > 0 else 1
        
        # 换手率
        avg_turnover = (volume / 1e8).rolling(window=5).mean()
        indicators['turnover_rate'] = avg_turnover.iloc[-1] if not pd.isna(avg_turnover.iloc[-1]) else 0
        
        # MACD
        exp12 = close.ewm(span=12, adjust=False).mean()
        exp26 = close.ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9, adjust=False).mean()
        indicators['macd'] = macd.iloc[-1]
        indicators['macd_signal'] = signal.iloc[-1]
        indicators['macd_hist'] = (macd - signal).iloc[-1]
        
        # 布林带位置
        ma20_close = close.rolling(window=20).mean()
        std20 = close.rolling(window=20).std()
        upper = ma20_close + 2 * std20
        lower = ma20_close - 2 * std20
        indicators['boll_position'] = (close.iloc[-1] - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1] + 1e-10)
        
        # ATR (波动率)
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=14).mean()
        indicators['atr_pct'] = atr.iloc[-1] / close.iloc[-1] * 100 if close.iloc[-1] > 0 else 0
        
        # 价格位置 (相对52周高低)
        high_52w = high.rolling(window=min(252, len(high))).max()
        low_52w = low.rolling(window=min(252, len(low))).min()
        indicators['price_position'] = (close.iloc[-1] - low_52w.iloc[-1]) / (high_52w.iloc[-1] - low_52w.iloc[-1] + 1e-10)
        
        return indicators
        
    except Exception as e:
        logger.debug(f"计算技术指标失败 {code}: {e}")
        return {}


def get_fundamental_data(jq, code: str, date: str):
    """获取基本面数据"""
    try:
        # 估值数据
        valuation = jq.get_valuation(code, end_date=date, count=1)
        
        fundamentals = {}
        
        if valuation is not None and len(valuation) > 0:
            fundamentals['pe'] = valuation['pe_ratio'].values[0] if 'pe_ratio' in valuation.columns else 0
            fundamentals['pb'] = valuation['pb_ratio'].values[0] if 'pb_ratio' in valuation.columns else 0
            fundamentals['ps'] = valuation['ps_ratio'].values[0] if 'ps_ratio' in valuation.columns else 0
            fundamentals['market_cap'] = valuation['market_cap'].values[0] if 'market_cap' in valuation.columns else 0
            fundamentals['turnover_ratio'] = valuation['turnover_ratio'].values[0] if 'turnover_ratio' in valuation.columns else 0
        
        # 财务指标
        q = jq.query(jq.indicator).filter(jq.indicator.code == code)
        indicator = jq.get_fundamentals(q, date=date)
        
        if indicator is not None and len(indicator) > 0:
            fundamentals['roe'] = indicator['roe'].values[0] if 'roe' in indicator.columns else 0
            fundamentals['roa'] = indicator['roa'].values[0] if 'roa' in indicator.columns else 0
            fundamentals['gross_margin'] = indicator['gross_profit_margin'].values[0] if 'gross_profit_margin' in indicator.columns else 0
            fundamentals['net_margin'] = indicator['net_profit_margin'].values[0] if 'net_profit_margin' in indicator.columns else 0
        
        return fundamentals
        
    except Exception as e:
        logger.debug(f"获取基本面数据失败 {code}: {e}")
        return {}


def get_financing_data(jq, code: str, date: str):
    """获取融资融券数据"""
    try:
        end_date = pd.to_datetime(date)
        start_date = end_date - timedelta(days=30)
        
        mtss = jq.get_mtss(
            code,
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=date
        )
        
        if mtss is None or len(mtss) < 2:
            return {'fin_change': 0}
        
        # 计算融资余额变化率
        fin_balance = mtss['fin_balance'] if 'fin_balance' in mtss.columns else mtss['rzye']
        fin_change = (fin_balance.iloc[-1] / fin_balance.iloc[0] - 1) * 100 if fin_balance.iloc[0] > 0 else 0
        
        return {'fin_change': fin_change}
        
    except Exception as e:
        return {'fin_change': 0}


def prepare_enhanced_training_data(output_path: str = 'results/training_data_v4_enhanced.csv'):
    """准备增强的训练数据"""
    jq = init_jqdata()
    if jq is None:
        logger.error("无法连接JQData")
        return
    
    # 加载原始数据
    original_path = Path('results/training_data_v4.csv')
    if not original_path.exists():
        logger.error(f"原始数据不存在: {original_path}")
        return
    
    df = pd.read_csv(original_path)
    logger.info(f"加载原始数据: {len(df)} 条")
    
    # 增强特征
    enhanced_records = []
    
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="提取增强特征"):
        code = row['code']
        date = row.get('prediction_date') or row.get('date')
        
        record = row.to_dict()
        
        # 获取技术指标
        tech = calculate_technical_indicators(jq, code, date)
        record.update(tech)
        
        # 获取基本面数据 (如果原始数据缺失)
        if pd.isna(record.get('roe')) or record.get('roe') == 0:
            fund = get_fundamental_data(jq, code, date)
            for k, v in fund.items():
                if k not in record or pd.isna(record[k]) or record[k] == 0:
                    record[k] = v
        
        # 获取融资融券数据
        if record.get('fin_change', 0) == 0:
            fin = get_financing_data(jq, code, date)
            record.update(fin)
        
        enhanced_records.append(record)
    
    # 保存增强数据
    enhanced_df = pd.DataFrame(enhanced_records)
    enhanced_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    logger.info(f"增强数据已保存: {output_path}")
    logger.info(f"总列数: {len(enhanced_df.columns)}")
    
    # 打印数据质量
    print("\n增强后数据质量:")
    print("="*60)
    for col in enhanced_df.columns:
        if enhanced_df[col].dtype in ['float64', 'int64']:
            non_zero = (enhanced_df[col] != 0).mean()
            null_rate = enhanced_df[col].isna().mean()
            print(f'{col:20s}: 非零={non_zero:5.1%}, 缺失={null_rate:5.1%}')
    
    return enhanced_df


if __name__ == "__main__":
    prepare_enhanced_training_data()
