"""
预测因子提取器 - 从历史高收益案例中提取“前一周锚点日”的预测性因子（周频）

核心逻辑：
1. 对于每个历史高收益案例（T时刻收益>=10%）
2. 获取T-1周时刻的因子数据（前一自然周的锚点交易日，动态适配节假日）
3. 这些因子才是真正能"预测"高收益的因子

这与之前的"描述性因子"完全不同：
- 描述性因子：分析高收益股票在T时刻有什么特征
- 预测性因子：分析T-1周时刻什么特征能预测T时刻的高收益
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)


@dataclass
class PredictiveFeature:
    """预测性特征"""
    code: str
    name: str
    prediction_date: str  # T-1周锚点日（预测日）
    target_date: str      # T时刻（目标日）
    target_return: float  # T时刻的实际收益
    is_high_return: bool  # 是否达到10%+
    
    # 基本面因子（T-5时刻）
    market_cap: float = 0.0
    pe_ratio: float = 0.0
    pb_ratio: float = 0.0
    roe: float = 0.0
    growth: float = 0.0       # 净利润增长
    revenue_growth: float = 0.0
    
    # 技术面因子（T-5时刻）
    momentum_5d: float = 0.0
    momentum_10d: float = 0.0
    momentum_20d: float = 0.0
    rel_strength: float = 0.0  # 相对位置
    rsi: float = 0.0
    volume_ratio: float = 0.0  # 量比
    
    # 资金面因子（T-5时刻）
    turnover_rate: float = 0.0
    fin_change: float = 0.0    # 融资余额变化
    on_billboard: int = 0      # 是否龙虎榜
    
    # 市场环境因子（T-5时刻）
    market_trend: float = 0.0  # 大盘趋势
    industry: str = ""


class PredictorFactorExtractor:
    """预测因子提取器"""

    WEEKLY_LABEL_THRESHOLD_PCT: float = 5.0  # 未来1周收益阈值（百分比）
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.jq = None
        self._init_jqdata()
    
    def _init_jqdata(self):
        """初始化JQData"""
        try:
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
    
    def get_trading_days(self, start_date: str, end_date: str) -> List[str]:
        """获取交易日列表"""
        days = self.jq.get_trade_days(start_date=start_date, end_date=end_date)
        return [d.strftime('%Y-%m-%d') for d in days]
    
    def get_trading_days_in_week(self, date: str) -> List[str]:
        """获取指定日期所属自然周的交易日列表（动态适配节假日）"""
        dt = datetime.strptime(date, "%Y-%m-%d").date()
        week_start = dt - timedelta(days=dt.weekday())  # Monday
        week_end = week_start + timedelta(days=6)       # Sunday
        return self.get_trading_days(str(week_start), str(week_end))

    def get_week_start_end(self, date: str) -> Optional[Tuple[str, str]]:
        """获取指定日期所属自然周的（首个交易日, 最后交易日）"""
        days = self.get_trading_days_in_week(date)
        if not days:
            return None
        return days[0], days[-1]

    def get_prev_week_anchor(self, date: str, lookback_weeks: int = 1) -> Optional[str]:
        """获取指定日期往前lookback_weeks周的锚点交易日（默认：前一周最后一个交易日）"""
        dt = datetime.strptime(date, "%Y-%m-%d").date()
        anchor = None

        for _ in range(max(1, int(lookback_weeks))):
            this_week_start = dt - timedelta(days=dt.weekday())
            prev_week_end = this_week_start - timedelta(days=1)
            prev_week_start = prev_week_end - timedelta(days=prev_week_end.weekday())

            trade_days = self.get_trading_days(str(prev_week_start), str(prev_week_end))
            if not trade_days:
                return None

            anchor = trade_days[-1]
            dt = prev_week_start  # 继续往前滚动一周

        return anchor

    def _get_close_on_or_before(self, code: str, date: str) -> Optional[float]:
        """获取不晚于date的最近一个交易日收盘价（用于处理date非交易日的情况）"""
        prices = self.jq.get_price(
            code,
            end_date=date,
            count=1,
            frequency='daily',
            fields=['close'],
            skip_paused=True,
            fq='post'
        )
        if prices is None or len(prices) == 0:
            return None
        return float(prices['close'].iloc[-1])

    def compute_future_week_return_pct(self, code: str, prediction_date: str, target_date: str) -> Optional[float]:
        """周频目标：从prediction_date（前一周锚点日）到target_date所属周的最后交易日的收益率（百分比）"""
        week_span = self.get_week_start_end(target_date)
        if not week_span:
            return None
        _, week_end = week_span

        start_close = self._get_close_on_or_before(code, prediction_date)
        end_close = self._get_close_on_or_before(code, week_end)
        if start_close is None or end_close is None or start_close <= 0:
            return None

        return (end_close / start_close - 1) * 100

    def get_t_minus_n_date(self, date: str, n: int = 5) -> str:
        """获取T-N交易日（兼容旧逻辑；V4.0周频版本不再作为主口径使用）"""
        end_dt = datetime.strptime(date, '%Y-%m-%d')
        start_dt = end_dt - timedelta(days=30)  # 往前找30天足够
        
        trading_days = self.get_trading_days(start_dt.strftime('%Y-%m-%d'), date)
        
        if len(trading_days) <= n:
            return trading_days[0]
        
        return trading_days[-(n+1)]  # T-N交易日
    
    def extract_factors_at_date(self, code: str, date: str) -> Dict:
        """提取指定日期的因子数据"""
        factors = {
            'code': code,
            'date': date,
        }
        
        try:
            # 基本面因子
            q = self.jq.query(
                self.jq.valuation.code,
                self.jq.valuation.market_cap,
                self.jq.valuation.pe_ratio,
                self.jq.valuation.pb_ratio,
                self.jq.valuation.turnover_ratio,
                self.jq.indicator.roe,
                self.jq.indicator.inc_net_profit_year_on_year,
                self.jq.indicator.inc_revenue_year_on_year,
            ).filter(
                self.jq.valuation.code == code
            )
            
            fund_df = self.jq.get_fundamentals(q, date=date)
            
            if fund_df is not None and not fund_df.empty:
                factors['market_cap'] = fund_df['market_cap'].iloc[0]
                factors['pe_ratio'] = fund_df['pe_ratio'].iloc[0]
                factors['pb_ratio'] = fund_df['pb_ratio'].iloc[0]
                factors['turnover_rate'] = fund_df['turnover_ratio'].iloc[0]
                factors['roe'] = fund_df['roe'].iloc[0]
                factors['growth'] = fund_df['inc_net_profit_year_on_year'].iloc[0]
                factors['revenue_growth'] = fund_df['inc_revenue_year_on_year'].iloc[0]
            
            # 技术面因子
            start_dt = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=60)
            prices = self.jq.get_price(
                code,
                start_date=start_dt.strftime('%Y-%m-%d'),
                end_date=date,
                frequency='daily',
                fields=['close', 'high', 'low', 'volume'],
                skip_paused=True,
                fq='post'
            )
            
            if prices is not None and len(prices) >= 20:
                close = prices['close']
                high = prices['high']
                low = prices['low']
                volume = prices['volume']
                
                # 动量
                factors['momentum_5d'] = (close.iloc[-1] / close.iloc[-5] - 1) * 100 if len(close) >= 5 else 0
                factors['momentum_10d'] = (close.iloc[-1] / close.iloc[-10] - 1) * 100 if len(close) >= 10 else 0
                factors['momentum_20d'] = (close.iloc[-1] / close.iloc[-20] - 1) * 100 if len(close) >= 20 else 0
                
                # 相对位置
                high_20 = high.tail(20).max()
                low_20 = low.tail(20).min()
                factors['rel_strength'] = (close.iloc[-1] - low_20) / (high_20 - low_20) * 100 if high_20 != low_20 else 50
                
                # RSI
                delta = close.diff()
                gain = delta.where(delta > 0, 0).tail(14).mean()
                loss = (-delta.where(delta < 0, 0)).tail(14).mean()
                factors['rsi'] = 100 - (100 / (1 + gain / loss)) if loss != 0 else 50
                
                # 量比
                avg_vol_5 = volume.tail(5).mean()
                avg_vol_20 = volume.tail(20).mean()
                factors['volume_ratio'] = avg_vol_5 / avg_vol_20 if avg_vol_20 > 0 else 1
            
            # 融资融券
            try:
                mtss_start = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=10)
                mtss = self.jq.get_mtss([code], start_date=mtss_start.strftime('%Y-%m-%d'), end_date=date)
                if mtss is not None and len(mtss) >= 2:
                    factors['fin_change'] = (mtss['fin_value'].iloc[-1] / mtss['fin_value'].iloc[0] - 1) * 100
                else:
                    factors['fin_change'] = 0
            except:
                factors['fin_change'] = 0
            
            # 龙虎榜
            try:
                billboard = self.jq.get_billboard_list(stock_list=[code], end_date=date, count=5)
                factors['on_billboard'] = 1 if billboard is not None and len(billboard) > 0 else 0
            except:
                factors['on_billboard'] = 0
            
            # 市场趋势（沪深300）
            try:
                bench = self.jq.get_price(
                    '000300.XSHG',
                    end_date=date,
                    count=20,
                    frequency='daily',
                    fields=['close'],
                    fq='post'
                )
                if bench is not None and len(bench) >= 20:
                    factors['market_trend'] = (bench['close'].iloc[-1] / bench['close'].iloc[0] - 1) * 100
                else:
                    factors['market_trend'] = 0
            except:
                factors['market_trend'] = 0
            
            # 行业
            try:
                industry = self.jq.get_industry(code, date)
                factors['industry'] = list(industry.get(code, {}).get('sw_l1', {}).values())[0] if industry else '未知'
            except:
                factors['industry'] = '未知'
                
        except Exception as e:
            logger.warning(f"提取因子失败 {code}@{date}: {e}")
        
        return factors
    
    def extract_from_historical_cases(self, cases_file: str,
                                      lookback_weeks: int = 1,
                                      lookback_days: int = 5,
                                      checkpoint_file: str = None, 
                                      resume: bool = True) -> pd.DataFrame:
        """从历史高收益案例中提取预测性因子（支持断点续传）
        
        Args:
            cases_file: 历史案例CSV文件路径
            lookback_weeks: 提前几个自然周获取因子（默认1周，周频主口径）
            lookback_days: 兼容参数（旧：提前几个交易日）；当lookback_weeks为None时才使用
            checkpoint_file: 断点文件路径（用于保存中间结果）
            resume: 是否从断点恢复
            
        Returns:
            DataFrame包含T-1周锚点日的预测性因子
        """
        print(f"\n{'='*60}")
        if lookback_weeks is not None:
            print(f"【预测因子提取】周频：从T-{lookback_weeks}周锚点日提取因子")
        else:
            print(f"【预测因子提取】兼容：从T-{lookback_days}交易日提取因子")
        print(f"{'='*60}")
        
        # 加载历史案例
        cases_df = pd.read_csv(cases_file)
        print(f"加载历史案例: {len(cases_df)} 条")
        
        # 检查点文件路径
        if checkpoint_file is None:
            checkpoint_file = cases_file.replace('.csv', f'_predictive_checkpoint.csv')
        
        # 尝试从断点恢复
        processed_codes = set()
        predictive_features = []  # 存储字典（从断点恢复）或PredictiveFeature对象（新提取）
        
        if resume and Path(checkpoint_file).exists():
            try:
                checkpoint_df = pd.read_csv(checkpoint_file)
                processed_codes = set(checkpoint_df['code'].astype(str) + '_' + checkpoint_df['target_date'].astype(str))
                # 保存为字典列表（便于后续保存）
                predictive_features = checkpoint_df.to_dict('records')
                print(f"从断点恢复: 已处理 {len(processed_codes)} 个案例")
            except Exception as e:
                logger.warning(f"读取断点文件失败: {e}，从头开始")
        
        # 提取预测因子（跳过已处理的）
        total = len(cases_df)
        checkpoint_interval = 10  # 每10个案例保存一次
        
        for idx, case in tqdm(cases_df.iterrows(), total=total, desc="提取预测因子", initial=len(processed_codes)):
            code = case['code']
            target_date = case['date']
            case_key = f"{code}_{target_date}"
            
            # 跳过已处理的案例
            if case_key in processed_codes:
                continue
            
            # 周频：目标收益=从前一周锚点日到本周周末交易日的收益（%）
            target_return = None
            
            # 获取预测日（周频：前一周锚点日）
            try:
                if lookback_weeks is not None:
                    prediction_date = self.get_prev_week_anchor(target_date, lookback_weeks=lookback_weeks)
                    if prediction_date is None:
                        raise ValueError("前一周锚点交易日为空")
                else:
                    prediction_date = self.get_t_minus_n_date(target_date, lookback_days)
            except Exception as e:
                if lookback_weeks is not None:
                    logger.warning(f"获取T-{lookback_weeks}周锚点日失败 {code}@{target_date}: {e}")
                else:
                    logger.warning(f"获取T-{lookback_days}日期失败 {code}@{target_date}: {e}")
                continue
            
            # 计算周度目标收益
            try:
                target_return = self.compute_future_week_return_pct(code, prediction_date, target_date)
            except Exception as e:
                logger.warning(f"计算周度目标收益失败 {code}@{prediction_date}->{target_date}: {e}")
                continue

            if target_return is None:
                logger.warning(f"计算周度目标收益为空 {code}@{prediction_date}->{target_date}")
                continue

            # 提取预测日因子
            factors = self.extract_factors_at_date(code, prediction_date)
            
            if not factors or 'market_cap' not in factors:
                logger.warning(f"提取因子失败 {code}@{prediction_date}")
                continue
            
            # 构建预测特征
            feature = PredictiveFeature(
                code=code,
                name=case.get('name', code),
                prediction_date=prediction_date,
                target_date=target_date,
                target_return=target_return,
                is_high_return=target_return >= self.WEEKLY_LABEL_THRESHOLD_PCT,
                market_cap=factors.get('market_cap', 0),
                pe_ratio=factors.get('pe_ratio', 0),
                pb_ratio=factors.get('pb_ratio', 0),
                roe=factors.get('roe', 0),
                growth=factors.get('growth', 0),
                revenue_growth=factors.get('revenue_growth', 0),
                momentum_5d=factors.get('momentum_5d', 0),
                momentum_10d=factors.get('momentum_10d', 0),
                momentum_20d=factors.get('momentum_20d', 0),
                rel_strength=factors.get('rel_strength', 50),
                rsi=factors.get('rsi', 50),
                volume_ratio=factors.get('volume_ratio', 1),
                turnover_rate=factors.get('turnover_rate', 0),
                fin_change=factors.get('fin_change', 0),
                on_billboard=factors.get('on_billboard', 0),
                market_trend=factors.get('market_trend', 0),
                industry=factors.get('industry', '未知'),
            )
            
            predictive_features.append(feature)
            processed_codes.add(case_key)
            
            # 定期保存断点（每处理checkpoint_interval个案例）
            if len(predictive_features) % checkpoint_interval == 0:
                try:
                    # 转换为字典列表（兼容对象和字典）
                    records = []
                    for f in predictive_features:
                        if isinstance(f, dict):
                            records.append(f)
                        else:
                            records.append(vars(f))
                    df_checkpoint = pd.DataFrame(records)
                    df_checkpoint.to_csv(checkpoint_file, index=False, encoding='utf-8-sig')
                    logger.debug(f"已保存断点: {len(predictive_features)} 个案例")
                except Exception as e:
                    logger.warning(f"保存断点失败: {e}")
        
        # 转换为DataFrame（兼容对象和字典）
        records = []
        for f in predictive_features:
            if isinstance(f, dict):
                records.append(f)
            else:
                records.append(vars(f))
        df = pd.DataFrame(records)
        
        # 保存最终结果和断点
        if len(df) > 0:
            try:
                df.to_csv(checkpoint_file, index=False, encoding='utf-8-sig')
                logger.info(f"断点文件已保存: {checkpoint_file}")
            except Exception as e:
                logger.warning(f"保存断点文件失败: {e}")
        
        print(f"\n提取完成: {len(df)} 条预测特征")
        print(f"高收益案例: {(df['is_high_return']).sum()} 条")
        
        return df
    
    def build_training_dataset(self, 
                               high_return_cases_file: str,
                               start_date: str,
                               end_date: str,
                               sample_size: int = 5000) -> pd.DataFrame:
        """构建训练数据集
        
        包括：
        1. 正样本：历史高收益案例的T-5因子
        2. 负样本：随机抽样的非高收益股票的因子
        
        Args:
            high_return_cases_file: 高收益案例文件
            start_date: 起始日期
            end_date: 结束日期
            sample_size: 负样本数量
        """
        print(f"\n{'='*60}")
        print(f"【构建训练数据集】")
        print(f"正样本来源: {high_return_cases_file}")
        print(f"负样本采样: {sample_size} 条")
        print(f"{'='*60}")
        
        # 提取正样本（高收益案例的T-5因子）
        positive_df = self.extract_from_historical_cases(high_return_cases_file)
        positive_df['label'] = 1
        
        # 采样负样本
        print(f"\n采样负样本...")
        dates = self.get_trading_days(start_date, end_date)
        sample_dates = np.random.choice(dates, min(50, len(dates)), replace=False)
        
        negative_samples = []
        
        for date in tqdm(sample_dates, desc="采样负样本"):
            # 获取股票池
            stocks = self.jq.get_all_securities(types=['stock'], date=date)
            stocks = stocks[~stocks.index.str.startswith('688')]
            stocks = stocks[~stocks['display_name'].str.contains('ST')]
            stock_list = stocks.index.tolist()
            
            # 随机抽样
            sample_codes = np.random.choice(stock_list, min(100, len(stock_list)), replace=False)
            
            for code in sample_codes:
                # 获取未来5日收益
                future_dt = datetime.strptime(date, '%Y-%m-%d') + timedelta(days=10)
                prices = self.jq.get_price(
                    code,
                    start_date=date,
                    end_date=future_dt.strftime('%Y-%m-%d'),
                    frequency='daily',
                    fields=['close'],
                    skip_paused=True,
                    fq='post'
                )
                
                if prices is None or len(prices) < 5:
                    continue
                
                future_return = (prices['close'].iloc[min(5, len(prices)-1)] / prices['close'].iloc[0] - 1) * 100
                
                # 只选择非高收益的样本
                if future_return >= 10:
                    continue
                
                # 提取因子
                factors = self.extract_factors_at_date(code, date)
                if not factors or 'market_cap' not in factors:
                    continue
                
                negative_samples.append({
                    'code': code,
                    'name': stocks.loc[code, 'display_name'] if code in stocks.index else code,
                    'prediction_date': date,
                    'target_date': date,
                    'target_return': future_return,
                    'is_high_return': False,
                    'label': 0,
                    **{k: v for k, v in factors.items() if k not in ['code', 'date']}
                })
                
                if len(negative_samples) >= sample_size:
                    break
            
            if len(negative_samples) >= sample_size:
                break
        
        negative_df = pd.DataFrame(negative_samples)
        print(f"负样本采集: {len(negative_df)} 条")
        
        # 合并数据集
        dataset = pd.concat([positive_df, negative_df], ignore_index=True)
        dataset = dataset.sample(frac=1).reset_index(drop=True)  # 打乱顺序
        
        print(f"\n最终数据集: {len(dataset)} 条")
        print(f"  正样本: {(dataset['label'] == 1).sum()} ({(dataset['label'] == 1).mean():.1%})")
        print(f"  负样本: {(dataset['label'] == 0).sum()} ({(dataset['label'] == 0).mean():.1%})")
        
        return dataset


def main():
    """测试预测因子提取"""
    extractor = PredictorFactorExtractor()
    
    # 从历史案例提取预测因子
    df = extractor.extract_from_historical_cases(
        'results/high_return_cases_full_train.csv',
        lookback_days=5
    )
    
    df.to_csv('results/predictive_features.csv', index=False, encoding='utf-8-sig')
    print(f"\n预测特征已保存: results/predictive_features.csv")


if __name__ == '__main__':
    main()
