#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
牛市高回报股票挖掘器

从历史数据中识别牛市期间，并提取牛市期间周收益≥10%的高回报股票案例。
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import logging
import json
from collections import defaultdict

# 项目根目录
TRQUANT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(TRQUANT_ROOT))

logger = logging.getLogger(__name__)


@dataclass
class HighReturnCase:
    """高回报案例"""
    code: str
    entry_date: str          # 买入日期
    exit_date: str           # 卖出日期
    horizon_name: str        # 周期类型：short/medium/long
    holding_days: int        # 持有天数
    return_pct: float        # 收益率（百分比）
    entry_price: float
    exit_price: float
    
    # 因子数据（T-1锚点）
    momentum_20d: float = 0.0
    momentum_5d: float = 0.0
    rel_position: float = 0.0
    market_cap: float = 0.0
    turnover_rate: float = 0.0
    roe: float = 0.0
    growth: float = 0.0
    
    # 早期识别信号
    signal_momentum_5d: float = 0.0
    signal_volume_ratio: float = 0.0
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'code': self.code,
            'entry_date': self.entry_date,
            'exit_date': self.exit_date,
            'horizon_name': self.horizon_name,
            'holding_days': self.holding_days,
            'return_pct': self.return_pct,
            'entry_price': self.entry_price,
            'exit_price': self.exit_price,
            'momentum_20d': self.momentum_20d,
            'momentum_5d': self.momentum_5d,
            'rel_position': self.rel_position,
            'market_cap': self.market_cap,
            'turnover_rate': self.turnover_rate,
            'roe': self.roe,
            'growth': self.growth,
            'signal_momentum_5d': self.signal_momentum_5d,
            'signal_volume_ratio': self.signal_volume_ratio,
        }


@dataclass
class HorizonConfig:
    """不同持有周期配置"""
    name: str
    window_days: int
    min_return_pct: float
    max_cases_per_stock: int = 50


@dataclass
class MinerConfig:
    """挖掘器全局配置"""
    horizons: List[HorizonConfig] = field(default_factory=lambda: [
        HorizonConfig(name='short', window_days=5, min_return_pct=8.0),
        HorizonConfig(name='medium', window_days=20, min_return_pct=18.0),
        HorizonConfig(name='long', window_days=60, min_return_pct=35.0),
    ])
    chunk_size: int = 40                 # get_price批量拉取的股票数
    buffer_days: int = 5                 # 额外向前补齐的交易日数量
    max_cases_total: Optional[int] = None
    enable_volume_signals: bool = True


class BullMarketHighReturnMiner:
    """牛市高回报股票挖掘器"""
    
    def __init__(
        self,
        min_return_pct: float = 10.0,
        config: Optional[MinerConfig] = None,
        verbose: bool = True
    ):
        """
        初始化
        
        Args:
            min_return_pct: 兼容旧参数，作为短周期收益率阈值默认值
            config: MinerConfig，可覆盖默认周期/批量设置
            verbose: 是否输出详细信息
        """
        self.config = config or MinerConfig()
        # 兼容旧参数：如果用户传入min_return_pct，则覆盖第一条 horizon
        if self.config.horizons:
            self.config.horizons[0].min_return_pct = min_return_pct
        self.verbose = verbose
        self.jq = None
        self.factor_extractor = None
        self._init_dependencies()
    
    def _init_dependencies(self):
        """初始化依赖（JQData、MarketRegimeDetector、PredictorFactorExtractor）"""
        try:
            # JQData
            import jqdatasdk as jq
            from config.config_manager import get_config_manager
            
            config_mgr = get_config_manager()
            jq_config = config_mgr.get_config('jqdata')
            jq.auth(jq_config.get('username'), jq_config.get('password'))
            self.jq = jq
            
            if self.verbose:
                print("✅ JQData连接成功")
        except Exception as e:
            logger.error(f"JQData连接失败: {e}")
            raise
        
        try:
            # PredictorFactorExtractor
            from core.advisor_v4.predictor_factor_extractor import PredictorFactorExtractor
            self.factor_extractor = PredictorFactorExtractor(verbose=False)
            if self.verbose:
                print("✅ PredictorFactorExtractor初始化成功")
        except Exception as e:
            logger.warning(f"PredictorFactorExtractor初始化失败: {e}")
            self.factor_extractor = None
    
    def get_trading_days(self, start_date: str, end_date: str) -> List[str]:
        """获取交易日列表"""
        days = self.jq.get_trade_days(start_date=start_date, end_date=end_date)
        return [d.strftime('%Y-%m-%d') for d in days]
    
    
    def extract_factors(self, code: str, entry_date: str) -> Dict[str, float]:
        """提取T-1周锚点日期的因子数据"""
        if self.factor_extractor is None:
            # 简化因子提取
            return {
                'momentum_20d': 0.0,
                'momentum_5d': 0.0,
                'rel_position': 0.0,
                'market_cap': 0.0,
                'turnover_rate': 0.0,
                'roe': 0.0,
                'growth': 0.0,
            }
        
        try:
            factors = self.factor_extractor.extract_factors_at_date(code, entry_date)
            return {
                'momentum_20d': factors.get('momentum_20d', 0.0),
                'momentum_5d': factors.get('momentum_5d', 0.0),
                'rel_position': factors.get('rel_position', 0.0),
                'market_cap': factors.get('market_cap', 0.0) / 100000000.0 if factors.get('market_cap') else 0.0,  # 转换为亿
                'turnover_rate': factors.get('turnover_rate', 0.0),
                'roe': factors.get('roe', 0.0),
                'growth': factors.get('growth', 0.0),
            }
        except Exception as e:
            logger.debug(f"提取{code}因子失败: {e}")
            return {
                'momentum_20d': 0.0,
                'momentum_5d': 0.0,
                'rel_position': 0.0,
                'market_cap': 0.0,
                'turnover_rate': 0.0,
                'roe': 0.0,
                'growth': 0.0,
            }
    
    # --------- 批量行情处理 ---------
    def _chunk_universe(self, universe: List[str]) -> List[List[str]]:
        chunk = self.config.chunk_size
        return [universe[i:i + chunk] for i in range(0, len(universe), chunk)]
    
    def _extract_field_dataframe(self, raw, field: str) -> Optional[pd.DataFrame]:
        """兼容JQData返回的Panel/MultiIndex DataFrame"""
        if raw is None:
            return None
        try:
            if isinstance(raw, dict) and field in raw:
                df = raw[field]
                if not isinstance(df.index, pd.DatetimeIndex):
                    df.index = pd.to_datetime(df.index)
                return df
            if hasattr(raw, 'items'):
                # pandas.Panel or xarray
                df = raw[field]
                if not isinstance(df.index, pd.DatetimeIndex):
                    df.index = pd.to_datetime(df.index)
                return df
            if isinstance(raw, pd.DataFrame):
                if {'time', 'code', field}.issubset(raw.columns):
                    df = raw.pivot(index='time', columns='code', values=field)
                    df.index = pd.to_datetime(df.index)
                    return df
                if isinstance(raw.columns, pd.MultiIndex):
                    return raw.xs(field, axis=1, level=0)
                if field in raw.columns:
                    df = raw[[field]]
                    if not isinstance(df.index, pd.DatetimeIndex):
                        df.index = pd.to_datetime(df.index)
                    return df
        except Exception as e:
            logger.debug(f"解析行情字段失败: {e}")
        return None
    
    def _fetch_price_panel(
        self,
        universe: List[str],
        start_date: str,
        end_date: str,
        fields: Optional[List[str]] = None
    ) -> Dict[str, pd.DataFrame]:
        """批量拉取行情，返回字段->DataFrame的映射"""
        fields = fields or ['close', 'volume']
        close_frames = []
        volume_frames = []
        buffer_days = max(h.window_days for h in self.config.horizons) + self.config.buffer_days
        start_dt = (datetime.strptime(start_date, '%Y-%m-%d') - timedelta(days=buffer_days)).strftime('%Y-%m-%d')
        
        for batch in self._chunk_universe(universe):
            try:
                panel = self.jq.get_price(
                    security=batch,
                    start_date=start_dt,
                    end_date=end_date,
                    frequency='daily',
                    fields=fields,
                    skip_paused=True,
                    fq='post'
                )
            except Exception as e:
                logger.warning(f"批量拉取行情失败({batch[0]}...): {e}")
                continue
            
            close_df = self._extract_field_dataframe(panel, 'close')
            if close_df is not None:
                close_frames.append(close_df)
            if 'volume' in fields:
                vol_df = self._extract_field_dataframe(panel, 'volume')
                if vol_df is not None:
                    volume_frames.append(vol_df)
        
        data = {}
        if close_frames:
            close_df = pd.concat(close_frames, axis=1).sort_index()
            close_df = close_df.loc[:, ~close_df.columns.duplicated(keep='first')]
            close_df = close_df.loc[start_date:end_date].ffill()
            data['close'] = close_df
        if volume_frames:
            vol_df = pd.concat(volume_frames, axis=1).sort_index()
            vol_df = vol_df.loc[:, ~vol_df.columns.duplicated(keep='first')]
            vol_df = vol_df.loc[start_date:end_date].fillna(0)
            data['volume'] = vol_df
        return data
    
    def _compute_signal_metrics(
        self,
        code: str,
        entry_idx: int,
        exit_idx: int,
        close_df: pd.DataFrame,
        volume_df: Optional[pd.DataFrame]
    ) -> Tuple[float, float]:
        """计算早期识别信号：5日动量、量能放大"""
        if entry_idx < 6:
            return 0.0, 0.0
        momentum = (close_df.iloc[entry_idx] / close_df.iloc[entry_idx - 5] - 1.0).get(code, 0.0) * 100
        volume_ratio = 0.0
        if self.config.enable_volume_signals and volume_df is not None and code in volume_df.columns:
            recent = volume_df.iloc[entry_idx - 1][code]
            base = volume_df.iloc[max(entry_idx - 6, 0):entry_idx - 1][code].mean()
            if base and base > 0:
                volume_ratio = float(recent / base)
        return float(momentum), float(volume_ratio)
    
    def summarize_cases(self, cases: List[HighReturnCase]) -> Dict[str, Any]:
        """统计案例共性因子及早期信号"""
        summary: Dict[str, Any] = {
            'total_cases': len(cases),
            'by_horizon': {},
            'factor_means': {},
            'signal_means': {}
        }
        if not cases:
            return summary
        
        df = pd.DataFrame([case.to_dict() for case in cases])
        for horizon in df['horizon_name'].unique():
            subset = df[df['horizon_name'] == horizon]
            summary['by_horizon'][horizon] = {
                'case_count': int(len(subset)),
                'avg_return_pct': float(subset['return_pct'].mean()),
                'median_return_pct': float(subset['return_pct'].median())
            }
        factor_cols = ['momentum_20d', 'momentum_5d', 'rel_position', 'market_cap', 'turnover_rate', 'roe', 'growth']
        for col in factor_cols:
            if col in df.columns:
                summary['factor_means'][col] = float(df[col].mean())
        summary['signal_means'] = {
            'signal_momentum_5d': float(df['signal_momentum_5d'].mean()),
            'signal_volume_ratio': float(df['signal_volume_ratio'].mean())
        }
        return summary
    
    def mine_high_return_cases(
        self,
        start_date: str,
        end_date: str,
        universe: Optional[List[str]] = None,
        summary_output: Optional[str] = None
    ) -> List[HighReturnCase]:
        """
        挖掘高回报案例（默认视为牛市窗口）
        
        Args:
            start_date: 开始日期（YYYY-MM-DD）
            end_date: 结束日期（YYYY-MM-DD）
            universe: 股票池（None表示全A股）
            summary_output: 若提供则导出JSON摘要
        
        Returns:
            高回报案例列表
        """
        if self.verbose:
            print(f"\n开始挖掘高回报案例...")
            print(f"  时间范围: {start_date} ~ {end_date}")
            print(f"  周期配置: {[f'{h.name}:{h.window_days}d@{h.min_return_pct}%' for h in self.config.horizons]}")
        
        # 获取股票池
        if universe is None:
            if self.verbose:
                print("  获取全A股股票池...")
            try:
                securities = self.jq.get_all_securities(types=['stock'], date=end_date)
                stocks = securities.index.tolist()
                universe = [
                    code for code in stocks
                    if 'ST' not in str(securities.loc[code, 'display_name']).upper()
                ]
                if self.verbose:
                    print(f"  股票池大小: {len(universe)}")
            except Exception as e:
                logger.error(f"获取股票池失败: {e}")
                return []
        
        if not universe:
            logger.warning("股票池为空")
            return []
        
        # 批量拉取行情
        panel = self._fetch_price_panel(universe, start_date, end_date, fields=['close', 'volume'])
        close_df = panel.get('close')
        if close_df is None or close_df.empty:
            logger.error("行情数据为空，无法继续")
            return []
        volume_df = panel.get('volume')
        
        cases: List[HighReturnCase] = []
        per_stock_counts: Dict[Tuple[str, str], int] = defaultdict(int)
        
        date_index = close_df.index
        if self.verbose:
            print(f"  有效交易日: {len(date_index)}")
        
        for horizon in self.config.horizons:
            window = horizon.window_days
            if len(date_index) <= window:
                continue
            for idx in range(window, len(date_index)):
                exit_date = date_index[idx]
                entry_idx = idx - window
                entry_date = date_index[entry_idx]
                
                entry_prices = close_df.iloc[entry_idx]
                exit_prices = close_df.iloc[idx]
                valid_mask = (entry_prices > 0) & (exit_prices > 0)
                if not valid_mask.any():
                    continue
                
                returns = (exit_prices / entry_prices - 1.0) * 100.0
                winners = returns[valid_mask & (returns >= horizon.min_return_pct)]
                if winners.empty:
                    continue
                
                winners = winners.sort_values(ascending=False)
                for code, ret in winners.items():
                    key = (code, horizon.name)
                    per_stock_counts[key] += 1
                    if horizon.max_cases_per_stock and per_stock_counts[key] > horizon.max_cases_per_stock:
                        continue
                    
                    factors = self.extract_factors(code, entry_date.strftime('%Y-%m-%d'))
                    sig_mom, sig_vol = self._compute_signal_metrics(code, entry_idx, idx, close_df, volume_df)
                    
                    case = HighReturnCase(
                        code=code,
                        entry_date=entry_date.strftime('%Y-%m-%d'),
                        exit_date=exit_date.strftime('%Y-%m-%d'),
                        horizon_name=horizon.name,
                        holding_days=window,
                        return_pct=float(ret),
                        entry_price=float(entry_prices[code]),
                        exit_price=float(exit_prices[code]),
                        signal_momentum_5d=sig_mom,
                        signal_volume_ratio=sig_vol,
                        **factors
                    )
                    cases.append(case)
                    
                    if self.config.max_cases_total and len(cases) >= self.config.max_cases_total:
                        break
                if self.config.max_cases_total and len(cases) >= self.config.max_cases_total:
                    break
            if self.config.max_cases_total and len(cases) >= self.config.max_cases_total:
                break
        
        if self.verbose:
            print(f"\n✅ 挖掘完成！共找到 {len(cases)} 个高回报案例")
            if cases:
                returns = [c.return_pct for c in cases]
                print(f"  平均收益率: {np.mean(returns):.2f}%")
                print(f"  中位数收益率: {np.median(returns):.2f}%")
        
        if summary_output:
            summary = self.summarize_cases(cases)
            output_path = Path(summary_output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            if self.verbose:
                print(f"  📊 已输出摘要: {output_path}")
        
        return cases
    
    def save_to_csv(self, cases: List[HighReturnCase], output_path: str):
        """保存到CSV文件"""
        if not cases:
            logger.warning("没有案例可保存")
            return
        
        df = pd.DataFrame([case.to_dict() for case in cases])
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        if self.verbose:
            print(f"\n✅ 已保存到: {output_file}")
            print(f"  案例数量: {len(cases)}")
            print(f"  文件大小: {output_file.stat().st_size / 1024:.2f} KB")


def main():
    """主函数：示例用法"""
    import argparse
    
    parser = argparse.ArgumentParser(description='挖掘牛市高回报股票案例')
    parser.add_argument('--start-date', type=str, default='2024-09-01', help='开始日期')
    parser.add_argument('--end-date', type=str, default='2025-09-13', help='结束日期')
    parser.add_argument('--min-return', type=float, default=10.0, help='最低收益率（%）')
    parser.add_argument('--output', type=str, default='data/bull_market_high_return_cases.csv', help='输出文件路径')
    parser.add_argument('--summary', type=str, default='data/bull_market_high_return_summary.json', help='摘要输出路径')
    parser.add_argument('--universe-size', type=int, default=1000, help='股票池大小（0表示全A股）')
    parser.add_argument('--chunk-size', type=int, default=40, help='行情批量拉取的股票数')
    parser.add_argument('--max-cases', type=int, default=0, help='限制总案例数，0表示不限')
    
    args = parser.parse_args()
    
    config = MinerConfig(
        chunk_size=args.chunk_size,
        max_cases_total=args.max_cases or None
    )
    # 创建挖掘器
    miner = BullMarketHighReturnMiner(min_return_pct=args.min_return, config=config, verbose=True)
    
    # 设置股票池（可选）
    universe = None
    if args.universe_size > 0:
        try:
            stocks = miner.jq.get_all_securities(types=['stock'], date=args.end_date).index.tolist()
            universe = stocks[:args.universe_size]
            print(f"使用股票池: {len(universe)}只股票")
        except Exception as e:
            print(f"⚠️ 获取股票池失败: {e}，将使用全A股")
    
    # 挖掘案例
    cases = miner.mine_high_return_cases(
        start_date=args.start_date,
        end_date=args.end_date,
        universe=universe,
        summary_output=args.summary
    )
    
    # 保存结果
    if cases:
        miner.save_to_csv(cases, args.output)
    else:
        print("⚠️ 未找到任何高回报案例")


if __name__ == '__main__':
    main()
