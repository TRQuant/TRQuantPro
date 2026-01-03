"""
高性能回测模块 v2 - 使用修复版HMM + GPU可选加速
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
    use_gpu: bool = False


@dataclass
class SignalResult:
    date: str
    signal_type: str
    composite_score: float
    hmm_state: str
    hmm_aligned: bool
    confidence_level: str
    returns_5d: float = 0.0
    returns_20d: float = 0.0
    correct_5d: bool = False
    correct_20d: bool = False


class DataCache:
    def __init__(self):
        self._mem = {}
    
    def _key(self, name, params):
        return hashlib.md5(f"{name}_{json.dumps(params, sort_keys=True)}".encode()).hexdigest()
    
    def get(self, name, params):
        key = self._key(name, params)
        if key in self._mem:
            return self._mem[key]
        f = CACHE_DIR / f"{key}.pkl"
        if f.exists():
            try:
                with open(f, 'rb') as fp:
                    data = pickle.load(fp)
                self._mem[key] = data
                return data
            except:
                pass
        return None
    
    def set(self, name, params, data):
        key = self._key(name, params)
        self._mem[key] = data
        try:
            with open(CACHE_DIR / f"{key}.pkl", 'wb') as f:
                pickle.dump(data, f)
        except:
            pass


class FastBacktesterV2:
    """高性能回测器 v2 - 修复版HMM"""
    
    def __init__(self, use_gpu: bool = False):
        self._jq = None
        self._cache = DataCache()
        self.use_gpu = use_gpu
        
    def _ensure_jqdata(self):
        if self._jq is None:
            import jqdatasdk as jq
            with open("/home/taotao/dev/QuantTest/TRQuant/config/jqdata_config.json") as f:
                cfg = json.load(f)
            jq.auth(cfg['username'], cfg['password'])
            self._jq = jq
    
    def _load_data(self, config):
        params = {'s': config.start_date, 'e': config.end_date, 'b': config.benchmark, 'v': 2}
        if config.use_cache:
            cached = self._cache.get('price_v2', params)
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
                self._cache.set('price_v2', params, df)
        return df
    
    def _calc_indicators(self, df):
        """向量化计算技术指标"""
        logger.info("计算技术指标...")
        close = df['close']
        
        # MA
        for p in [5, 10, 20, 50, 60, 120, 250]:
            df[f'ma{p}'] = close.rolling(p).mean()
        
        # 收益率和动量
        df['returns'] = close.pct_change() * 100
        df['momentum_20d'] = close.pct_change(20) * 100
        df['returns_5d'] = close.pct_change(5).shift(-5) * 100
        df['returns_20d'] = close.pct_change(20).shift(-20) * 100
        
        # MA位置
        df['price_vs_ma20'] = (close / df['ma20'] - 1) * 100
        df['price_vs_ma60'] = (close / df['ma60'] - 1) * 100
        
        # 波动率
        df['volatility'] = df['returns'].rolling(20).std() * np.sqrt(252)
        
        # 综合得分
        df['short_score'] = np.where(df['ma5'] > df['ma10'], 20, -20)
        df['medium_score'] = np.where(df['ma20'] > df['ma50'], 25, -25) + np.where(close > df['ma20'], 15, -15)
        df['long_score'] = np.where(df['ma60'] > df['ma120'], 30, -30) + np.where(df['ma120'] > df['ma250'], 25, -25)
        df['composite_score'] = df['short_score'] * 0.2 + df['medium_score'] * 0.3 + df['long_score'] * 0.5
        
        return df
    
    def _calc_hmm_fixed(self, df, use_cache=True, cache_params=None):
        """使用修复版HMM计算状态"""
        logger.info("计算修复版HMM状态...")
        
        # 检查缓存
        if use_cache and cache_params:
            cached = self._cache.get('hmm_fixed', cache_params)
            if cached is not None:
                logger.info("从缓存加载HMM状态")
                df['hmm_state'] = cached['states']
                df['hmm_confidence'] = cached['confidence']
                return df
        
        try:
            from core.hmm_fixed import FixedHMM
            hmm = FixedHMM(use_gpu=self.use_gpu)
            
            states = ['unknown'] * len(df)
            confidences = [0.0] * len(df)
            
            window = 80  # HMM需要60天数据+20天预热
            
            for i in range(window, len(df)):
                try:
                    window_df = df.iloc[:i+1].copy()
                    result = hmm.analyze(window_df)
                    if result:
                        states[i] = result.current_state.to_english()
                        confidences[i] = result.confidence
                except:
                    pass
            
            df['hmm_state'] = states
            df['hmm_confidence'] = confidences
            
            # 缓存
            if use_cache and cache_params:
                self._cache.set('hmm_fixed', cache_params, {
                    'states': states,
                    'confidence': confidences
                })
                
        except Exception as e:
            logger.warning(f"HMM计算失败: {e}")
            df['hmm_state'] = 'unknown'
            df['hmm_confidence'] = 0.0
        
        return df
    
    def _generate_signals(self, df, config):
        """生成信号"""
        logger.info("生成信号...")
        start_dt = pd.to_datetime(config.start_date)
        end_dt = pd.to_datetime(config.end_date)
        mask = (df.index >= start_dt) & (df.index <= end_dt)
        sampled = df[mask].iloc[::config.sample_interval]
        
        signals = []
        for _, row in sampled.iterrows():
            # 技术信号
            sig_type = 'bullish' if row['composite_score'] > 20 else ('bearish' if row['composite_score'] < -20 else 'neutral')
            
            # HMM对齐（严格匹配）
            hmm = row.get('hmm_state', 'unknown')
            hmm_aligned = (sig_type == 'bullish' and hmm == 'bull') or (sig_type == 'bearish' and hmm == 'bear')
            
            # 置信度（基于HMM和技术一致性）
            if hmm_aligned:
                confidence_level = "high"
            elif hmm != 'unknown':
                confidence_level = "medium"
            else:
                confidence_level = "low"
            
            # 收益
            r5 = row.get('returns_5d', 0.0)
            r20 = row.get('returns_20d', 0.0)
            
            # 准确性判断
            if sig_type == 'bullish':
                c5, c20 = r5 > 0 if pd.notna(r5) else False, r20 > 0 if pd.notna(r20) else False
            elif sig_type == 'bearish':
                c5, c20 = r5 < 0 if pd.notna(r5) else False, r20 < 0 if pd.notna(r20) else False
            else:
                c5, c20 = abs(r5) < 3 if pd.notna(r5) else False, abs(r20) < 5 if pd.notna(r20) else False
            
            signals.append(SignalResult(
                date=row['date_str'], signal_type=sig_type, composite_score=row['composite_score'],
                hmm_state=hmm, hmm_aligned=hmm_aligned, confidence_level=confidence_level,
                returns_5d=r5 if pd.notna(r5) else 0, returns_20d=r20 if pd.notna(r20) else 0,
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
        
        # HMM计算
        cache_params = {'s': config.start_date, 'e': config.end_date, 'type': 'hmm_fixed_v2'}
        df = self._calc_hmm_fixed(df, use_cache=config.use_cache, cache_params=cache_params)
        
        signals = self._generate_signals(df, config)
        
        total = len(signals)
        if total == 0:
            return {"error": "无信号"}
        
        # 统计
        high_conf = [s for s in signals if s.confidence_level == 'high']
        med_conf = [s for s in signals if s.confidence_level == 'medium']
        low_conf = [s for s in signals if s.confidence_level == 'low']
        hmm_aligned = [s for s in signals if s.hmm_aligned]
        
        elapsed = (datetime.now() - start).total_seconds()
        
        def calc_acc(lst, attr):
            return sum(1 for s in lst if getattr(s, attr)) / len(lst) * 100 if lst else 0
        
        return {
            "total_signals": total,
            "accuracy_5d": calc_acc(signals, 'correct_5d'),
            "accuracy_20d": calc_acc(signals, 'correct_20d'),
            "high_confidence_signals": len(high_conf),
            "high_confidence_accuracy_5d": calc_acc(high_conf, 'correct_5d'),
            "high_confidence_accuracy_20d": calc_acc(high_conf, 'correct_20d'),
            "medium_confidence_signals": len(med_conf),
            "medium_confidence_accuracy_5d": calc_acc(med_conf, 'correct_5d'),
            "medium_confidence_accuracy_20d": calc_acc(med_conf, 'correct_20d'),
            "low_confidence_signals": len(low_conf),
            "low_confidence_accuracy_5d": calc_acc(low_conf, 'correct_5d'),
            "low_confidence_accuracy_20d": calc_acc(low_conf, 'correct_20d'),
            "hmm_aligned_signals": len(hmm_aligned),
            "hmm_aligned_accuracy_5d": calc_acc(hmm_aligned, 'correct_5d'),
            "hmm_aligned_accuracy_20d": calc_acc(hmm_aligned, 'correct_20d'),
            "elapsed_seconds": elapsed
        }
