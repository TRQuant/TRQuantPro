"""
高性能回测模块 - 使用缓存和批量计算
"""
import logging
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
import numpy as np
import pandas as pd
from pathlib import Path
import pickle

logger = logging.getLogger(__name__)

CACHE_DIR = Path("/home/taotao/dev/QuantTest/TRQuant/.cache/backtest")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class FastBacktestConfig:
    start_date: str = "2023-01-01"
    end_date: str = "2024-08-16"
    benchmark: str = "000001.XSHG"
    sample_interval: int = 5
    use_cache: bool = True


@dataclass
class SignalResult:
    date: str
    signal_type: str
    composite_score: float
    short_score: float
    medium_score: float
    long_score: float
    hmm_state: str
    hmm_aligned: bool
    high_confidence: bool
    medium_confidence: bool
    confidence_level: str
    returns_5d: float = 0.0
    returns_20d: float = 0.0
    correct_5d: bool = False
    correct_20d: bool = False


class DataCache:
    def __init__(self):
        self._memory_cache = {}
    
    def _get_key(self, name, params):
        return hashlib.md5(f"{name}_{json.dumps(params, sort_keys=True)}".encode()).hexdigest()
    
    def get(self, name, params):
        key = self._get_key(name, params)
        if key in self._memory_cache:
            return self._memory_cache[key]
        cache_file = CACHE_DIR / f"{key}.pkl"
        if cache_file.exists():
            try:
                import warnings
                with warnings.catch_warnings():
                    warnings.filterwarnings('ignore', category=DeprecationWarning,
                                            module='pandas.compat.pickle_compat')
                    with open(cache_file, 'rb') as f:
                        data = pickle.load(f)
                self._memory_cache[key] = data
                return data
            except:
                pass
        return None
    
    def set(self, name, params, data):
        key = self._get_key(name, params)
        self._memory_cache[key] = data
        try:
            with open(CACHE_DIR / f"{key}.pkl", 'wb') as f:
                pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            logger.warning(f"缓存保存失败: {e}")


class FastBacktester:
    def __init__(self):
        self._jq = None
        self._cache = DataCache()
        
    def _ensure_jqdata(self):
        if self._jq is None:
            import jqdatasdk as jq
            with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
                cfg = json.load(f)
            jq.auth(cfg['username'], cfg['password'])
            self._jq = jq
    
    def _load_data(self, config):
        params = {'s': config.start_date, 'e': config.end_date, 'b': config.benchmark}
        if config.use_cache:
            cached = self._cache.get('price', params)
            if cached is not None:
                logger.info(f"从缓存加载: {len(cached)}行")
                return cached
        
        self._ensure_jqdata()
        start_dt = datetime.strptime(config.start_date, '%Y-%m-%d') - timedelta(days=300)
        end_dt = datetime.strptime(config.end_date, '%Y-%m-%d') + timedelta(days=120)
        
        logger.info(f"下载数据: {start_dt.date()} ~ {end_dt.date()}")
        df = self._jq.get_price(config.benchmark, start_date=start_dt.strftime('%Y-%m-%d'),
                                end_date=end_dt.strftime('%Y-%m-%d'), frequency='daily',
                                fields=['open', 'high', 'low', 'close', 'volume'])
        
        if df is not None and not df.empty:
            df.index = pd.to_datetime(df.index)
            df['date_str'] = df.index.strftime('%Y-%m-%d')
            if config.use_cache:
                self._cache.set('price', params, df)
        return df
    
    def _calc_indicators(self, df):
        logger.info("计算技术指标...")
        close = df['close']
        
        # MA
        for p in [5, 10, 20, 50, 60, 120, 250]:
            df[f'ma{p}'] = close.rolling(p).mean()
        
        # 收益率
        df['returns_5d'] = close.pct_change(5).shift(-5) * 100
        df['returns_20d'] = close.pct_change(20).shift(-20) * 100
        
        # RSI
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df['rsi'] = 100 - (100 / (1 + gain / loss))
        
        # MACD
        exp1 = close.ewm(span=12).mean()
        exp2 = close.ewm(span=26).mean()
        df['macd_hist'] = (exp1 - exp2) - (exp1 - exp2).ewm(span=9).mean()
        
        # 得分
        df['short_score'] = np.where(df['ma5'] > df['ma10'], 20, -20) + np.where(df['macd_hist'] > 0, 15, -15)
        df['medium_score'] = np.where(df['ma20'] > df['ma50'], 25, -25) + np.where(close > df['ma20'], 15, -15)
        df['long_score'] = np.where(df['ma60'] > df['ma120'], 30, -30) + np.where(df['ma120'] > df['ma250'], 25, -25)
        df['composite_score'] = df['short_score'] * 0.2 + df['medium_score'] * 0.3 + df['long_score'] * 0.5
        
        return df
    
    def _calc_hmm(self, df):
        logger.info("计算HMM状态...")
        try:
            from core.trend_ml import SimpleHMM
            hmm = SimpleHMM(use_astock_params=True)
            window = 60
            states = []
            for i in range(len(df)):
                if i < window:
                    states.append('unknown')
                else:
                    try:
                        result = hmm.analyze(df.iloc[i-window:i+1])
                        if result:
                            state_map = {'牛市': 'bull', '熊市': 'bear', '震荡': 'sideways'}
                            states.append(state_map.get(result.current_state.value, 'unknown'))
                        else:
                            states.append('unknown')
                    except:
                        states.append('unknown')
            df['hmm_state'] = states
        except Exception as e:
            logger.warning(f"HMM失败: {e}")
            df['hmm_state'] = 'unknown'
        return df
    
    def _generate_signals(self, df, config):
        logger.info("生成信号...")
        start_dt = pd.to_datetime(config.start_date)
        end_dt = pd.to_datetime(config.end_date)
        mask = (df.index >= start_dt) & (df.index <= end_dt)
        sampled = df[mask].iloc[::config.sample_interval]
        
        signals = []
        for _, row in sampled.iterrows():
            sig_type = 'bullish' if row['composite_score'] > 20 else ('bearish' if row['composite_score'] < -20 else 'neutral')
            long_sig = 'bullish' if row['long_score'] > 20 else ('bearish' if row['long_score'] < -20 else 'neutral')
            med_sig = 'bullish' if row['medium_score'] > 15 else ('bearish' if row['medium_score'] < -15 else 'neutral')
            
            hmm = row.get('hmm_state', 'unknown')
            # HMM对齐判断 - 放宽条件
            # 1. HMM牛市 + 信号不是看空 = 对齐
            # 2. HMM熊市 + 信号不是看多 = 对齐
            # 3. HMM震荡 + 信号中性 = 对齐
            hmm_aligned = (hmm == 'bull' and sig_type != 'bearish') or                          (hmm == 'bear' and sig_type != 'bullish') or                          (hmm == 'sideways' and sig_type == 'neutral')
            long_aligned = (sig_type == 'bullish' and long_sig == 'bullish') or (sig_type == 'bearish' and long_sig == 'bearish')
            med_aligned = (sig_type == 'bullish' and med_sig == 'bullish') or (sig_type == 'bearish' and med_sig == 'bearish')
            
            high_conf = hmm_aligned and long_aligned
            med_conf = (hmm_aligned or (long_aligned and med_aligned)) and not high_conf
            conf_level = "high" if high_conf else ("medium" if med_conf else "low")
            
            r5 = row.get('returns_5d', 0.0)
            r20 = row.get('returns_20d', 0.0)
            
            if sig_type == 'bullish':
                c5, c20 = r5 > 0 if pd.notna(r5) else False, r20 > 0 if pd.notna(r20) else False
            elif sig_type == 'bearish':
                c5, c20 = r5 < 0 if pd.notna(r5) else False, r20 < 0 if pd.notna(r20) else False
            else:
                c5, c20 = abs(r5) < 3 if pd.notna(r5) else False, abs(r20) < 5 if pd.notna(r20) else False
            
            signals.append(SignalResult(
                date=row['date_str'], signal_type=sig_type, composite_score=row['composite_score'],
                short_score=row['short_score'], medium_score=row['medium_score'], long_score=row['long_score'],
                hmm_state=hmm, hmm_aligned=hmm_aligned, high_confidence=high_conf, medium_confidence=med_conf,
                confidence_level=conf_level, returns_5d=r5 if pd.notna(r5) else 0, returns_20d=r20 if pd.notna(r20) else 0,
                correct_5d=c5, correct_20d=c20
            ))
        return signals
    
    def run(self, config=None):
        if config is None:
            config = FastBacktestConfig()
        
        start = datetime.now()
        df = self._load_data(config)
        if df is None or df.empty:
            return {"error": "无数据"}
        
        df = self._calc_indicators(df)
        
        # HMM缓存
        params = {'s': config.start_date, 'e': config.end_date, 'type': 'hmm'}
        cached_hmm = self._cache.get('hmm', params) if config.use_cache else None
        if cached_hmm is not None:
            df['hmm_state'] = cached_hmm
        else:
            df = self._calc_hmm(df)
            if config.use_cache:
                self._cache.set('hmm', params, df['hmm_state'].tolist())
        
        signals = self._generate_signals(df, config)
        
        total = len(signals)
        if total == 0:
            return {"error": "无信号"}
        
        high_conf = [s for s in signals if s.high_confidence]
        med_conf = [s for s in signals if s.medium_confidence]
        low_conf = [s for s in signals if s.confidence_level == 'low']
        hmm_aligned = [s for s in signals if s.hmm_aligned]
        
        elapsed = (datetime.now() - start).total_seconds()
        
        return {
            "total_signals": total,
            "accuracy_5d": sum(1 for s in signals if s.correct_5d) / total * 100,
            "accuracy_20d": sum(1 for s in signals if s.correct_20d) / total * 100,
            "high_confidence_signals": len(high_conf),
            "high_confidence_accuracy_5d": sum(1 for s in high_conf if s.correct_5d) / len(high_conf) * 100 if high_conf else 0,
            "medium_confidence_signals": len(med_conf),
            "medium_confidence_accuracy_5d": sum(1 for s in med_conf if s.correct_5d) / len(med_conf) * 100 if med_conf else 0,
            "low_confidence_signals": len(low_conf),
            "low_confidence_accuracy_5d": sum(1 for s in low_conf if s.correct_5d) / len(low_conf) * 100 if low_conf else 0,
            "hmm_aligned_signals": len(hmm_aligned),
            "hmm_aligned_accuracy_5d": sum(1 for s in hmm_aligned if s.correct_5d) / len(hmm_aligned) * 100 if hmm_aligned else 0,
            "elapsed_seconds": elapsed
        }
