# -*- coding: utf-8 -*-
"""
特征扩展器 - 扩展预测模型的特征维度

功能：
1. 技术指标扩展（MACD、KDJ、BOLL、CCI等）
2. 基本面指标扩展（PB、PS、ROA等）
3. 市场微观结构（资金流向、换手率变化）
4. 行业/板块特征

扩展后特征数：14 -> 35+
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class FeatureExpander:
    """特征扩展器"""
    
    # 原始特征（来自XGBoostPredictor）
    ORIGINAL_FEATURES = [
        'market_cap',        # 市值
        'roe',               # ROE
        'growth',            # 净利润增长率
        'momentum_5d',       # 5日动量
        'momentum_10d',      # 10日动量
        'momentum_20d',      # 20日动量
        'rel_strength',      # 相对强度
        'rsi',               # RSI
        'volume_ratio',      # 成交量比率
        'fin_change',        # 融资余额变化
        'turnover_rate',     # 换手率
        'on_billboard',      # 是否上龙虎榜
        'concept_count',     # 概念数量
        'market_trend',      # 市场趋势
    ]
    
    # 扩展特征定义
    EXPANDED_FEATURES = {
        # Level 1: 基础技术指标
        'level1': [
            'macd',              # MACD
            'macd_signal',       # MACD信号线
            'macd_hist',         # MACD柱状图
            'kdj_k',             # KDJ-K
            'kdj_d',             # KDJ-D
            'kdj_j',             # KDJ-J
            'boll_upper',        # 布林上轨
            'boll_middle',       # 布林中轨
            'boll_lower',        # 布林下轨
            'boll_width',        # 布林带宽
            'cci',               # CCI
        ],
        
        # Level 2: 进阶技术指标
        'level2': [
            'atr',               # 平均真实波幅
            'volatility_20d',    # 20日波动率
            'obv',               # 能量潮
            'obv_change',        # OBV变化率
            'adx',               # 趋向指标
            'di_plus',           # +DI
            'di_minus',          # -DI
            'wr',                # 威廉指标
            'mfi',               # 资金流量指标
        ],
        
        # Level 3: 基本面指标
        'level3': [
            'pb',                # 市净率
            'ps',                # 市销率
            'pcf',               # 市现率
            'roa',               # 总资产收益率
            'roic',              # 投入资本回报率
            'current_ratio',     # 流动比率
            'quick_ratio',       # 速动比率
            'debt_to_equity',    # 资产负债率
            'revenue_growth',    # 营收增长率
            'gross_margin',      # 毛利率
        ],
        
        # Level 4: 市场微观结构
        'level4': [
            'big_order_ratio',       # 大单比例
            'main_force_inflow',     # 主力净流入
            'turnover_change',       # 换手率变化
            'price_volume_corr',     # 量价相关性
            'buying_pressure',       # 买盘压力
            'selling_pressure',      # 卖盘压力
            'spread',                # 买卖价差
        ],
        
        # Level 5: 行业/板块特征
        'level5': [
            'industry_rank',         # 行业内排名
            'industry_momentum',     # 行业动量
            'sector_rotation',       # 板块轮动信号
            'relative_to_index',     # 相对指数强度
        ],
    }
    
    def __init__(self, 
                 level: int = 2,
                 use_jqdata: bool = True):
        """
        Args:
            level: 扩展级别 (1-5)
            use_jqdata: 是否使用JQData获取数据
        """
        self.level = level
        self.use_jqdata = use_jqdata
        self.jq = None
        
        # 确定要计算的特征
        self.features_to_expand = []
        for i in range(1, level + 1):
            level_key = f'level{i}'
            if level_key in self.EXPANDED_FEATURES:
                self.features_to_expand.extend(self.EXPANDED_FEATURES[level_key])
        
        logger.info(f"特征扩展器初始化: level={level}, 扩展特征数={len(self.features_to_expand)}")
    
    def _init_jqdata(self):
        """初始化JQData连接"""
        if self.jq is not None:
            return True
        
        try:
            from config.config_manager import get_config_manager
            import jqdatasdk as jq
            
            cm = get_config_manager()
            jq_config = cm.get_config('jqdata')
            jq.auth(jq_config['username'], jq_config['password'])
            
            self.jq = jq
            return True
        except Exception as e:
            logger.warning(f"JQData初始化失败: {e}")
            return False
    
    def expand_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """扩展特征
        
        Args:
            df: 输入DataFrame，需包含code和prediction_date列
            
        Returns:
            扩展后的DataFrame
        """
        result_df = df.copy()
        
        # 确保有必要的列
        if 'code' not in result_df.columns or 'prediction_date' not in result_df.columns:
            logger.warning("缺少code或prediction_date列，使用模拟数据")
            return self._expand_with_simulated_data(result_df)
        
        # 尝试使用JQData
        if self.use_jqdata and self._init_jqdata():
            try:
                return self._expand_with_jqdata(result_df)
            except Exception as e:
                logger.warning(f"JQData扩展失败: {e}，使用模拟数据")
        
        # 回退到模拟数据
        return self._expand_with_simulated_data(result_df)
    
    def _expand_with_jqdata(self, df: pd.DataFrame) -> pd.DataFrame:
        """使用JQData扩展特征"""
        from tqdm import tqdm
        
        result_df = df.copy()
        
        # 初始化新特征列
        for feature in self.features_to_expand:
            if feature not in result_df.columns:
                result_df[feature] = np.nan
        
        # 按股票分组处理
        codes = result_df['code'].unique()
        
        for code in tqdm(codes, desc="扩展特征"):
            mask = result_df['code'] == code
            dates = result_df.loc[mask, 'prediction_date'].tolist()
            
            if not dates:
                continue
            
            # 获取价格数据（用于技术指标）
            min_date = min(dates)
            max_date = max(dates)
            
            # 往前多取60天的数据用于计算指标
            start_date = (pd.to_datetime(min_date) - timedelta(days=90)).strftime('%Y-%m-%d')
            
            try:
                price_df = self.jq.get_price(
                    code,
                    start_date=start_date,
                    end_date=max_date,
                    frequency='daily',
                    fields=['open', 'high', 'low', 'close', 'volume', 'money'],
                    skip_paused=False,
                    fq='post'
                )
                
                if price_df is None or len(price_df) < 20:
                    continue
                
                # 计算技术指标
                indicators = self._calculate_technical_indicators(price_df)
                
                # 填充到结果DataFrame
                for date in dates:
                    if date in indicators.index:
                        row_mask = (result_df['code'] == code) & (result_df['prediction_date'] == date)
                        for feature in self.features_to_expand:
                            if feature in indicators.columns:
                                result_df.loc[row_mask, feature] = indicators.loc[date, feature]
            
            except Exception as e:
                logger.debug(f"获取{code}数据失败: {e}")
                continue
        
        # 获取基本面数据（如果level >= 3）
        if self.level >= 3:
            result_df = self._add_fundamental_features(result_df)
        
        # 填充缺失值
        for feature in self.features_to_expand:
            if feature in result_df.columns:
                result_df[feature] = result_df[feature].fillna(result_df[feature].median())
        
        return result_df
    
    def _calculate_technical_indicators(self, price_df: pd.DataFrame) -> pd.DataFrame:
        """计算技术指标"""
        df = price_df.copy()
        
        close = df['close']
        high = df['high']
        low = df['low']
        volume = df['volume']
        
        # Level 1: 基础技术指标
        if self.level >= 1:
            # MACD
            exp1 = close.ewm(span=12, adjust=False).mean()
            exp2 = close.ewm(span=26, adjust=False).mean()
            df['macd'] = exp1 - exp2
            df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
            df['macd_hist'] = df['macd'] - df['macd_signal']
            
            # KDJ
            low_min = low.rolling(window=9).min()
            high_max = high.rolling(window=9).max()
            rsv = (close - low_min) / (high_max - low_min + 1e-10) * 100
            df['kdj_k'] = rsv.ewm(com=2, adjust=False).mean()
            df['kdj_d'] = df['kdj_k'].ewm(com=2, adjust=False).mean()
            df['kdj_j'] = 3 * df['kdj_k'] - 2 * df['kdj_d']
            
            # 布林带
            df['boll_middle'] = close.rolling(window=20).mean()
            std = close.rolling(window=20).std()
            df['boll_upper'] = df['boll_middle'] + 2 * std
            df['boll_lower'] = df['boll_middle'] - 2 * std
            df['boll_width'] = (df['boll_upper'] - df['boll_lower']) / (df['boll_middle'] + 1e-10)
            
            # CCI
            tp = (high + low + close) / 3
            tp_ma = tp.rolling(window=14).mean()
            tp_std = tp.rolling(window=14).std()
            df['cci'] = (tp - tp_ma) / (0.015 * tp_std + 1e-10)
        
        # Level 2: 进阶技术指标
        if self.level >= 2:
            # ATR
            tr1 = high - low
            tr2 = abs(high - close.shift(1))
            tr3 = abs(low - close.shift(1))
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            df['atr'] = tr.rolling(window=14).mean()
            
            # 20日波动率
            df['volatility_20d'] = close.pct_change().rolling(window=20).std() * np.sqrt(252)
            
            # OBV
            obv = (volume * np.where(close > close.shift(1), 1, 
                                     np.where(close < close.shift(1), -1, 0))).cumsum()
            df['obv'] = obv
            df['obv_change'] = obv.pct_change(periods=5) * 100
            
            # ADX
            plus_dm = high.diff()
            minus_dm = -low.diff()
            plus_dm[plus_dm < 0] = 0
            minus_dm[minus_dm < 0] = 0
            
            tr_smooth = tr.rolling(window=14).sum()
            plus_di = 100 * (plus_dm.rolling(window=14).sum() / (tr_smooth + 1e-10))
            minus_di = 100 * (minus_dm.rolling(window=14).sum() / (tr_smooth + 1e-10))
            
            df['di_plus'] = plus_di
            df['di_minus'] = minus_di
            dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di + 1e-10)
            df['adx'] = dx.rolling(window=14).mean()
            
            # 威廉指标
            df['wr'] = (high_max - close) / (high_max - low_min + 1e-10) * -100
            
            # MFI
            tp = (high + low + close) / 3
            money_flow = tp * volume
            positive_flow = money_flow.where(tp > tp.shift(1), 0).rolling(window=14).sum()
            negative_flow = money_flow.where(tp < tp.shift(1), 0).rolling(window=14).sum()
            mfi = 100 - (100 / (1 + positive_flow / (negative_flow + 1e-10)))
            df['mfi'] = mfi
        
        # 设置索引为日期字符串
        df.index = df.index.strftime('%Y-%m-%d')
        
        return df
    
    def _add_fundamental_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """添加基本面特征"""
        result_df = df.copy()
        
        # 基本面特征（Level 3）
        fundamental_features = self.EXPANDED_FEATURES.get('level3', [])
        
        codes = result_df['code'].unique()
        
        for code in codes:
            mask = result_df['code'] == code
            dates = result_df.loc[mask, 'prediction_date'].unique()
            
            for date in dates:
                try:
                    # 获取估值数据
                    valuation = self.jq.get_valuation(
                        code, 
                        end_date=date, 
                        fields=['pb_ratio', 'ps_ratio', 'pcf_ratio'],
                        count=1
                    )
                    
                    if valuation is not None and len(valuation) > 0:
                        row_mask = (result_df['code'] == code) & (result_df['prediction_date'] == date)
                        result_df.loc[row_mask, 'pb'] = valuation['pb_ratio'].values[0]
                        result_df.loc[row_mask, 'ps'] = valuation['ps_ratio'].values[0]
                        result_df.loc[row_mask, 'pcf'] = valuation['pcf_ratio'].values[0]
                    
                    # 获取财务指标
                    q = self.jq.query(
                        self.jq.indicator
                    ).filter(
                        self.jq.indicator.code == code
                    )
                    indicator = self.jq.get_fundamentals(q, date=date)
                    
                    if indicator is not None and len(indicator) > 0:
                        row_mask = (result_df['code'] == code) & (result_df['prediction_date'] == date)
                        if 'roa' in indicator.columns:
                            result_df.loc[row_mask, 'roa'] = indicator['roa'].values[0]
                        if 'roe' not in result_df.columns or pd.isna(result_df.loc[row_mask, 'roe']).all():
                            if 'roe' in indicator.columns:
                                result_df.loc[row_mask, 'roe'] = indicator['roe'].values[0]
                        if 'gross_profit_margin' in indicator.columns:
                            result_df.loc[row_mask, 'gross_margin'] = indicator['gross_profit_margin'].values[0]
                
                except Exception as e:
                    logger.debug(f"获取{code}基本面数据失败: {e}")
                    continue
        
        return result_df
    
    def _expand_with_simulated_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """使用模拟数据扩展（用于测试或JQData不可用时）"""
        result_df = df.copy()
        n = len(result_df)
        
        np.random.seed(42)
        
        for feature in self.features_to_expand:
            if feature not in result_df.columns:
                # 根据特征类型生成合理的模拟值
                if feature in ['macd', 'macd_signal', 'macd_hist']:
                    result_df[feature] = np.random.uniform(-2, 2, n)
                elif feature in ['kdj_k', 'kdj_d', 'kdj_j']:
                    result_df[feature] = np.random.uniform(0, 100, n)
                elif feature in ['boll_width']:
                    result_df[feature] = np.random.uniform(0, 0.2, n)
                elif feature in ['cci', 'wr']:
                    result_df[feature] = np.random.uniform(-100, 100, n)
                elif feature in ['atr']:
                    result_df[feature] = np.random.uniform(0.5, 5, n)
                elif feature in ['volatility_20d']:
                    result_df[feature] = np.random.uniform(0.1, 0.5, n)
                elif feature in ['adx', 'mfi']:
                    result_df[feature] = np.random.uniform(0, 100, n)
                elif feature in ['pb', 'ps', 'pcf']:
                    result_df[feature] = np.random.uniform(0.5, 10, n)
                elif feature in ['roa', 'roic']:
                    result_df[feature] = np.random.uniform(-5, 20, n)
                elif feature in ['current_ratio', 'quick_ratio']:
                    result_df[feature] = np.random.uniform(0.5, 3, n)
                elif feature in ['debt_to_equity']:
                    result_df[feature] = np.random.uniform(0, 100, n)
                elif feature in ['revenue_growth', 'gross_margin']:
                    result_df[feature] = np.random.uniform(-20, 50, n)
                elif feature in ['big_order_ratio', 'buying_pressure', 'selling_pressure']:
                    result_df[feature] = np.random.uniform(0, 1, n)
                elif feature in ['main_force_inflow']:
                    result_df[feature] = np.random.uniform(-100, 100, n)
                elif feature in ['turnover_change', 'price_volume_corr']:
                    result_df[feature] = np.random.uniform(-1, 1, n)
                elif feature in ['industry_rank']:
                    result_df[feature] = np.random.uniform(0, 100, n)
                elif feature in ['industry_momentum', 'sector_rotation', 'relative_to_index']:
                    result_df[feature] = np.random.uniform(-10, 10, n)
                else:
                    result_df[feature] = np.random.uniform(-1, 1, n)
        
        return result_df
    
    def get_all_feature_columns(self) -> List[str]:
        """获取所有特征列（原始 + 扩展）"""
        return self.ORIGINAL_FEATURES + self.features_to_expand
    
    def get_expanded_features(self) -> List[str]:
        """获取扩展的特征列"""
        return self.features_to_expand
    
    def get_feature_info(self) -> Dict:
        """获取特征信息"""
        return {
            'level': self.level,
            'original_features': len(self.ORIGINAL_FEATURES),
            'expanded_features': len(self.features_to_expand),
            'total_features': len(self.get_all_feature_columns()),
            'expanded_list': self.features_to_expand,
        }


# ============================================================
# 快速特征扩展（不使用JQData，基于已有数据计算）
# ============================================================

class QuickFeatureExpander:
    """快速特征扩展器 - 基于已有价格数据计算"""
    
    def __init__(self):
        pass
    
    def expand_from_price_data(self, 
                               df: pd.DataFrame,
                               price_col: str = 'close',
                               high_col: str = 'high',
                               low_col: str = 'low',
                               volume_col: str = 'volume') -> pd.DataFrame:
        """从价格数据扩展特征
        
        Args:
            df: 输入DataFrame，需包含价格和成交量数据
            
        Returns:
            扩展后的DataFrame
        """
        result_df = df.copy()
        
        if price_col not in df.columns:
            logger.warning(f"缺少{price_col}列，无法扩展")
            return result_df
        
        close = df[price_col]
        
        # 基础技术指标
        # MACD
        exp1 = close.ewm(span=12, adjust=False).mean()
        exp2 = close.ewm(span=26, adjust=False).mean()
        result_df['macd'] = exp1 - exp2
        result_df['macd_signal'] = result_df['macd'].ewm(span=9, adjust=False).mean()
        result_df['macd_hist'] = result_df['macd'] - result_df['macd_signal']
        
        # 布林带
        result_df['boll_middle'] = close.rolling(window=20).mean()
        std = close.rolling(window=20).std()
        result_df['boll_upper'] = result_df['boll_middle'] + 2 * std
        result_df['boll_lower'] = result_df['boll_middle'] - 2 * std
        result_df['boll_width'] = (result_df['boll_upper'] - result_df['boll_lower']) / (result_df['boll_middle'] + 1e-10)
        
        if high_col in df.columns and low_col in df.columns:
            high = df[high_col]
            low = df[low_col]
            
            # KDJ
            low_min = low.rolling(window=9).min()
            high_max = high.rolling(window=9).max()
            rsv = (close - low_min) / (high_max - low_min + 1e-10) * 100
            result_df['kdj_k'] = rsv.ewm(com=2, adjust=False).mean()
            result_df['kdj_d'] = result_df['kdj_k'].ewm(com=2, adjust=False).mean()
            result_df['kdj_j'] = 3 * result_df['kdj_k'] - 2 * result_df['kdj_d']
            
            # CCI
            tp = (high + low + close) / 3
            tp_ma = tp.rolling(window=14).mean()
            tp_std = tp.rolling(window=14).std()
            result_df['cci'] = (tp - tp_ma) / (0.015 * tp_std + 1e-10)
            
            # ATR
            tr1 = high - low
            tr2 = abs(high - close.shift(1))
            tr3 = abs(low - close.shift(1))
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            result_df['atr'] = tr.rolling(window=14).mean()
        
        # 波动率
        result_df['volatility_20d'] = close.pct_change().rolling(window=20).std() * np.sqrt(252)
        
        # OBV
        if volume_col in df.columns:
            volume = df[volume_col]
            obv = (volume * np.where(close > close.shift(1), 1, 
                                     np.where(close < close.shift(1), -1, 0))).cumsum()
            result_df['obv'] = obv
            result_df['obv_change'] = obv.pct_change(periods=5) * 100
        
        return result_df


# ============================================================
# 测试代码
# ============================================================

if __name__ == "__main__":
    print("测试特征扩展器...")
    
    # 创建模拟数据
    np.random.seed(42)
    n = 100
    
    df = pd.DataFrame({
        'code': [f'000001.XSHE'] * n,
        'prediction_date': pd.date_range('2024-01-01', periods=n, freq='D').strftime('%Y-%m-%d').tolist(),
        'market_cap': np.random.uniform(100, 1000, n),
        'roe': np.random.uniform(5, 20, n),
        'growth': np.random.uniform(-10, 30, n),
        'momentum_5d': np.random.uniform(-5, 10, n),
        'momentum_10d': np.random.uniform(-8, 15, n),
        'momentum_20d': np.random.uniform(-10, 20, n),
        'rel_strength': np.random.uniform(30, 70, n),
        'rsi': np.random.uniform(30, 70, n),
        'volume_ratio': np.random.uniform(0.8, 1.5, n),
        'fin_change': np.random.uniform(-5, 10, n),
        'turnover_rate': np.random.uniform(1, 5, n),
        'on_billboard': np.random.randint(0, 2, n),
        'concept_count': np.random.randint(1, 8, n),
        'market_trend': np.random.uniform(-2, 2, n),
        'label': np.random.randint(0, 2, n),
    })
    
    print(f"原始数据: {df.shape}")
    print(f"原始列: {df.columns.tolist()}")
    
    # 测试Level 1扩展
    expander = FeatureExpander(level=1, use_jqdata=False)
    expanded_df = expander.expand_features(df)
    
    print(f"\nLevel 1 扩展后: {expanded_df.shape}")
    print(f"扩展特征: {expander.get_expanded_features()}")
    print(f"特征信息: {expander.get_feature_info()}")
    
    # 测试Level 2扩展
    expander2 = FeatureExpander(level=2, use_jqdata=False)
    expanded_df2 = expander2.expand_features(df)
    
    print(f"\nLevel 2 扩展后: {expanded_df2.shape}")
    print(f"扩展特征数: {len(expander2.get_expanded_features())}")
    
    print("\n测试完成!")
