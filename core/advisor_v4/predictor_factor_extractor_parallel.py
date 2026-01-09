# -*- coding: utf-8 -*-
"""
预测因子提取器 - 并行+GPU批量加速版本
======================================

优化策略：
1. 多线程并行：利用JQData的3个并发连接，分段并行提取
2. 批量处理：批量获取价格数据，减少API调用次数
3. GPU批量加速：对技术指标计算（RSI、动量、移动平均等）使用GPU批量计算
4. 向量化计算：使用PyTorch向量化操作，一次计算多个股票

性能提升：
- 原来：1024个案例，每个1.7秒，总计约30分钟
- 并行提取：3个线程并行，每个案例约0.6秒，总计约10分钟（3倍加速）
- GPU批量计算：50个案例一批，一次性计算，可再提升2-3倍
- 总计：从30分钟降至3-5分钟（6-10倍加速）
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from tqdm import tqdm
import logging
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import threading
from functools import partial
import warnings

# GPU加速（可选）
try:
    import torch
    if torch.cuda.is_available():
        DEVICE = torch.device('cuda')
        USE_GPU = True
    else:
        DEVICE = torch.device('cpu')
        USE_GPU = False
except ImportError:
    USE_GPU = False
    DEVICE = None
    torch = None

logger = logging.getLogger(__name__)


def calculate_technical_indicators_gpu(prices: pd.DataFrame) -> Dict:
    """使用GPU计算技术指标（单个股票，向后兼容）
    
    注意：此函数用于向后兼容，实际使用批量GPU计算器
    """
    if not USE_GPU or prices is None or len(prices) < 20:
        return _calculate_technical_indicators_cpu(prices)
    
    try:
        # 检查是否在子进程中（无法使用fork的CUDA）
        import multiprocessing as mp
        if mp.current_process().name != 'MainProcess':
            # 在子进程中，尝试使用spawn初始化的GPU
            try:
                if torch.cuda.is_available():
                    device = torch.device('cuda')
                else:
                    return _calculate_technical_indicators_cpu(prices)
            except:
                return _calculate_technical_indicators_cpu(prices)
        else:
            device = DEVICE
        
        close = torch.tensor(prices['close'].values, dtype=torch.float32, device=device)
        high = torch.tensor(prices['high'].values, dtype=torch.float32, device=device)
        low = torch.tensor(prices['low'].values, dtype=torch.float32, device=device)
        volume = torch.tensor(prices['volume'].values, dtype=torch.float32, device=device)
        
        factors = {}
        
        # 动量（向量化计算）
        if len(close) >= 5:
            factors['momentum_5d'] = ((close[-1] / close[-5] - 1) * 100).cpu().item()
        if len(close) >= 10:
            factors['momentum_10d'] = ((close[-1] / close[-10] - 1) * 100).cpu().item()
        if len(close) >= 20:
            factors['momentum_20d'] = ((close[-1] / close[-20] - 1) * 100).cpu().item()
        
        # 相对位置
        if len(high) >= 20:
            high_20 = high[-20:].max()
            low_20 = low[-20:].min()
            factors['rel_strength'] = ((close[-1] - low_20) / (high_20 - low_20) * 100).cpu().item() if high_20 != low_20 else 50.0
        
        # RSI（GPU向量化）
        if len(close) >= 14:
            delta = close[1:] - close[:-1]
            gain = torch.where(delta > 0, delta, torch.tensor(0.0, device=device))[-14:].mean()
            loss = (-torch.where(delta < 0, delta, torch.tensor(0.0, device=device)))[-14:].mean()
            factors['rsi'] = (100 - (100 / (1 + gain / loss))).cpu().item() if loss.item() > 0 else 50.0
        
        # 量比
        if len(volume) >= 20:
            avg_vol_5 = volume[-5:].mean()
            avg_vol_20 = volume[-20:].mean()
            factors['volume_ratio'] = (avg_vol_5 / avg_vol_20).cpu().item() if avg_vol_20.item() > 0 else 1.0
        
        return factors
        
    except Exception as e:
        logger.warning(f"GPU计算失败，使用CPU: {e}")
        return _calculate_technical_indicators_cpu(prices)


def _calculate_technical_indicators_cpu(prices: pd.DataFrame) -> Dict:
    """CPU计算技术指标（原方法）"""
    if prices is None or len(prices) < 20:
        return {}
    
    factors = {}
    close = prices['close']
    high = prices['high']
    low = prices['low']
    volume = prices['volume']
    
    # 动量
    if len(close) >= 5:
        factors['momentum_5d'] = (close.iloc[-1] / close.iloc[-5] - 1) * 100
    if len(close) >= 10:
        factors['momentum_10d'] = (close.iloc[-1] / close.iloc[-10] - 1) * 100
    if len(close) >= 20:
        factors['momentum_20d'] = (close.iloc[-1] / close.iloc[-20] - 1) * 100
    
    # 相对位置
    if len(high) >= 20:
        high_20 = high.tail(20).max()
        low_20 = low.tail(20).min()
        factors['rel_strength'] = (close.iloc[-1] - low_20) / (high_20 - low_20) * 100 if high_20 != low_20 else 50
    
    # RSI
    if len(close) >= 14:
        delta = close.diff()
        gain = delta.where(delta > 0, 0).tail(14).mean()
        loss = (-delta.where(delta < 0, 0)).tail(14).mean()
        factors['rsi'] = 100 - (100 / (1 + gain / loss)) if loss != 0 else 50
    
    # 量比
    if len(volume) >= 20:
        avg_vol_5 = volume.tail(5).mean()
        avg_vol_20 = volume.tail(20).mean()
        factors['volume_ratio'] = avg_vol_5 / avg_vol_20 if avg_vol_20 > 0 else 1
    
    return factors


# 线程本地存储JQData连接（每个线程独立连接）
_thread_local = threading.local()

def _get_jq_client():
    """获取线程本地的JQData客户端"""
    if not hasattr(_thread_local, 'jq'):
        import jqdatasdk as jq
        from config.config_manager import get_config_manager
        
        config_mgr = get_config_manager()
        jq_config = config_mgr.get_config('jqdata')
        jq.auth(jq_config.get('username'), jq_config.get('password'))
        _thread_local.jq = jq
    
    return _thread_local.jq


def _get_prev_week_anchor(target_date: str, jq, lookback_weeks: int = 1) -> Optional[str]:
    """周频：获取前一周锚点交易日（默认：前一周最后一个交易日）"""
    dt = datetime.strptime(target_date, '%Y-%m-%d').date()
    anchor = None

    for _ in range(max(1, int(lookback_weeks))):
        this_week_start = dt - timedelta(days=dt.weekday())
        prev_week_end = this_week_start - timedelta(days=1)
        prev_week_start = prev_week_end - timedelta(days=prev_week_end.weekday())

        trade_days = jq.get_trade_days(start_date=str(prev_week_start), end_date=str(prev_week_end))
        trade_days = [d.strftime('%Y-%m-%d') for d in trade_days]
        if not trade_days:
            return None
        anchor = trade_days[-1]
        dt = prev_week_start

    return anchor


def _extract_price_data_only(args: Tuple) -> Tuple[str, Optional[pd.DataFrame]]:
    """仅提取价格数据（用于批量GPU计算）
    
    Returns:
        (case_key, prices_df) 元组
    """
    case_dict, lookback_weeks, lookback_days, checkpoint_file = args
    
    try:
        jq = _get_jq_client()
        code = case_dict['code']
        target_date = case_dict['date']
        case_key = f"{code}_{target_date}"
        
        # 获取预测日期
        if lookback_weeks is not None:
            prediction_date = _get_prev_week_anchor(target_date, jq, lookback_weeks=lookback_weeks)
        else:
            end_dt = datetime.strptime(target_date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=30)
            trading_days = jq.get_trade_days(start_date=start_dt.strftime('%Y-%m-%d'), end_date=target_date)
            trading_days = [d.strftime('%Y-%m-%d') for d in trading_days]
            if len(trading_days) <= lookback_days:
                return (case_key, None)
            prediction_date = trading_days[-(lookback_days+1)]
        
        if prediction_date is None:
            return (case_key, None)
        
        # 提取价格数据
        start_dt = datetime.strptime(prediction_date, '%Y-%m-%d') - timedelta(days=60)
        prices = jq.get_price(
            code,
            start_date=start_dt.strftime('%Y-%m-%d'),
            end_date=prediction_date,
            frequency='daily',
            fields=['close', 'high', 'low', 'volume'],
            skip_paused=True,
            fq='post'
        )
        
        return (case_key, prices if prices is not None and len(prices) >= 20 else None)
        
    except Exception as e:
        logger.warning(f"提取价格数据失败 {case_dict.get('code', 'unknown')}: {e}")
        case_key = f"{case_dict.get('code', 'unknown')}_{case_dict.get('date', 'unknown')}"
        return (case_key, None)


def _extract_factors_worker(code: str, date: str, jq=None) -> Dict:
    """提取单个股票的因子（工作函数）
    
    Args:
        code: 股票代码
        date: 日期
        jq: JQData客户端（如果为None，使用线程本地客户端）
    """
    if jq is None:
        jq = _get_jq_client()
    
    factors = {
        'code': code,
        'date': date,
    }
    
    try:
        # 基本面因子（批量查询，减少API调用）
        q = jq.query(
            jq.valuation.code,
            jq.valuation.market_cap,
            jq.valuation.pe_ratio,
            jq.valuation.pb_ratio,
            jq.valuation.turnover_ratio,
            jq.indicator.roe,
            jq.indicator.inc_net_profit_year_on_year,
            jq.indicator.inc_revenue_year_on_year,
        ).filter(jq.valuation.code == code)
        
        fund_df = jq.get_fundamentals(q, date=date)
        
        if fund_df is not None and not fund_df.empty:
            factors['market_cap'] = fund_df['market_cap'].iloc[0]
            factors['pe_ratio'] = fund_df['pe_ratio'].iloc[0]
            factors['pb_ratio'] = fund_df['pb_ratio'].iloc[0]
            factors['turnover_rate'] = fund_df['turnover_ratio'].iloc[0]
            factors['roe'] = fund_df['roe'].iloc[0]
            factors['growth'] = fund_df['inc_net_profit_year_on_year'].iloc[0]
            factors['revenue_growth'] = fund_df['inc_revenue_year_on_year'].iloc[0]
        
        # 技术面因子（优先使用GPU，如果可用）
        start_dt = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=60)
        prices = jq.get_price(
            code,
            start_date=start_dt.strftime('%Y-%m-%d'),
            end_date=date,
            frequency='daily',
            fields=['close', 'high', 'low', 'volume'],
            skip_paused=True,
            fq='post'
        )
        
        if prices is not None and len(prices) >= 20:
            # 优先使用GPU计算技术指标（如果可用）
            if USE_GPU:
                tech_factors = calculate_technical_indicators_gpu(prices)
            else:
                tech_factors = _calculate_technical_indicators_cpu(prices)
            factors.update(tech_factors)
        
        # 融资融券
        try:
            mtss_start = datetime.strptime(date, '%Y-%m-%d') - timedelta(days=10)
            mtss = jq.get_mtss([code], start_date=mtss_start.strftime('%Y-%m-%d'), end_date=date)
            if mtss is not None and len(mtss) >= 2:
                factors['fin_change'] = (mtss['fin_value'].iloc[-1] / mtss['fin_value'].iloc[0] - 1) * 100
            else:
                factors['fin_change'] = 0
        except:
            factors['fin_change'] = 0
        
        # 龙虎榜
        try:
            billboard = jq.get_billboard_list(stock_list=[code], end_date=date, count=5)
            factors['on_billboard'] = 1 if billboard is not None and len(billboard) > 0 else 0
        except:
            factors['on_billboard'] = 0
        
        # 市场趋势（沪深300）
        try:
            bench = jq.get_price(
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
            industry = jq.get_industry(code, date)
            factors['industry'] = list(industry.get(code, {}).get('sw_l1', {}).values())[0] if industry else '未知'
        except:
            factors['industry'] = '未知'
            
    except Exception as e:
        logger.warning(f"提取因子失败 {code}@{date}: {e}")
    
    return factors


def _extract_factors_with_cached_tech(args: Tuple, tech_indicators: Dict) -> Optional[Dict]:
    """提取因子，使用缓存的技术指标（用于批量GPU计算后的合并）"""
    case_dict, lookback_weeks, lookback_days, checkpoint_file = args
    
    try:
        jq = _get_jq_client()
        code = case_dict['code']
        target_date = case_dict['date']
        target_return = case_dict['return_5d']
        
        # 获取预测日期（与_extract_price_data_only相同逻辑）
        if lookback_weeks is not None:
            prediction_date = _get_prev_week_anchor(target_date, jq, lookback_weeks=lookback_weeks)
        else:
            end_dt = datetime.strptime(target_date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=30)
            trading_days = jq.get_trade_days(start_date=start_dt.strftime('%Y-%m-%d'), end_date=target_date)
            trading_days = [d.strftime('%Y-%m-%d') for d in trading_days]
            if len(trading_days) <= lookback_days:
                return None
            prediction_date = trading_days[-(lookback_days+1)]
        
        if prediction_date is None:
            return None
        
        # 提取其他因子（基本面、融资融券等）
        factors = _extract_factors_worker(code, prediction_date, jq)
        
        if not factors or 'market_cap' not in factors:
            return None
        
        # 合并技术指标（从缓存，覆盖可能已经计算的技术指标）
        if tech_indicators:
            factors.update(tech_indicators)
        
        # 构建结果
        result = {
            'code': code,
            'name': case_dict.get('name', code),
            'prediction_date': prediction_date,
            'target_date': target_date,
            'target_return': target_return,
            'is_high_return': target_return >= 10,
            **factors
        }
        
        return result
        
    except Exception as e:
        logger.warning(f"提取因子失败 {case_dict.get('code', 'unknown')}: {e}")
        return None


def _extract_single_case(args: Tuple) -> Optional[Dict]:
    """提取单个案例的因子（用于并行处理，线程版本）
    
    注意：此函数在子线程中运行，使用线程本地JQData连接
    当不使用GPU批量加速时使用此函数
    """
    case_dict, lookback_weeks, lookback_days, checkpoint_file = args
    
    try:
        # 获取线程本地的JQData客户端
        jq = _get_jq_client()
        
        code = case_dict['code']
        target_date = case_dict['date']
        target_return = case_dict['return_5d']
        
        # 周频：预测日=前一周锚点交易日；兼容：T-N交易日
        if lookback_weeks is not None:
            prediction_date = _get_prev_week_anchor(target_date, jq, lookback_weeks=lookback_weeks)
            if prediction_date is None:
                return None
        else:
            end_dt = datetime.strptime(target_date, '%Y-%m-%d')
            start_dt = end_dt - timedelta(days=30)
            trading_days = jq.get_trade_days(start_date=start_dt.strftime('%Y-%m-%d'),
                                            end_date=target_date)
            trading_days = [d.strftime('%Y-%m-%d') for d in trading_days]

            if len(trading_days) <= lookback_days:
                return None

            prediction_date = trading_days[-(lookback_days+1)]
        
        # 提取因子
        factors = _extract_factors_worker(code, prediction_date, jq)
        
        if not factors or 'market_cap' not in factors:
            return None
        
        # 构建结果
        result = {
            'code': code,
            'name': case_dict.get('name', code),
            'prediction_date': prediction_date,
            'target_date': target_date,
            'target_return': target_return,
            'is_high_return': target_return >= 10,
            **factors
        }
        
        return result
        
    except Exception as e:
        logger.warning(f"提取因子失败 {case_dict.get('code', 'unknown')}: {e}")
        return None


class ParallelPredictorFactorExtractor:
    """并行预测因子提取器（支持GPU批量加速）"""
    
    def __init__(self, num_workers: int = 3, use_gpu: bool = True, batch_size: int = 50, verbose: bool = True):
        """
        Args:
            num_workers: 并行进程数（默认3，对应JQData的3个并发连接）
            use_gpu: 是否使用GPU加速技术指标计算
            batch_size: GPU批处理大小（默认50，可根据显存调整）
            verbose: 是否打印详细信息
        """
        self.num_workers = min(num_workers, 3)  # JQData最多3个连接
        self.use_gpu = use_gpu and USE_GPU
        self.batch_size = batch_size
        self.verbose = verbose
        
        # 初始化GPU批量计算器
        if self.use_gpu:
            try:
                from .gpu_accelerator import GPUTechnicalIndicatorCalculator
                self.gpu_calculator = GPUTechnicalIndicatorCalculator(
                    batch_size=self.batch_size,
                    use_gpu=True
                )
                if self.verbose:
                    print(f"✅ GPU批量加速已启用: {torch.cuda.get_device_name(0)}")
                    print(f"   GPU显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
                    print(f"   批处理大小: {self.batch_size}")
            except Exception as e:
                logger.warning(f"GPU计算器初始化失败: {e}，将使用单例GPU计算")
                self.gpu_calculator = None
        else:
            self.gpu_calculator = None
            if self.verbose:
                print(f"⚠️  GPU加速未启用（使用CPU）")
        
        if self.verbose:
            print(f"✅ 并行提取器初始化: {self.num_workers} 个线程")
    
    def extract_from_historical_cases(self, cases_file: str,
                                      lookback_weeks: int = 1,
                                      lookback_days: int = 5,
                                      checkpoint_file: Optional[str] = None,
                                      resume: bool = True) -> pd.DataFrame:
        """从历史高收益案例中并行提取预测性因子（支持GPU批量加速）
        
        Args:
            cases_file: 历史案例CSV文件路径
            lookback_weeks: 提前几个自然周获取因子（默认1周）
            lookback_days: 兼容参数（旧：提前几个交易日）
            checkpoint_file: 断点文件路径
            resume: 是否从断点恢复
            
        Returns:
            DataFrame包含T-1周锚点日的预测性因子
        """
        print(f"\n{'='*60}")
        if lookback_weeks is not None:
            print(f"【并行预测因子提取】周频：从T-{lookback_weeks}周锚点日提取因子")
        else:
            print(f"【并行预测因子提取】兼容：从T-{lookback_days}交易日提取因子")
        print(f"GPU批量加速: {'✅' if (self.use_gpu and self.gpu_calculator) else '❌'}, 并行数: {self.num_workers}")
        if self.use_gpu and self.gpu_calculator:
            print(f"GPU批处理大小: {self.batch_size}")
        print(f"{'='*60}")
        
        # 加载历史案例
        cases_df = pd.read_csv(cases_file)
        print(f"加载历史案例: {len(cases_df)} 条")
        
        # 检查点文件路径
        if checkpoint_file is None:
            checkpoint_file = cases_file.replace('.csv', f'_predictive_checkpoint_parallel.csv')
        
        # 尝试从断点恢复
        processed_codes = set()
        existing_results = []
        
        if resume and Path(checkpoint_file).exists():
            try:
                checkpoint_df = pd.read_csv(checkpoint_file)
                processed_codes = set(checkpoint_df['code'].astype(str) + '_' + checkpoint_df['target_date'].astype(str))
                existing_results = checkpoint_df.to_dict('records')
                print(f"从断点恢复: 已处理 {len(processed_codes)} 个案例")
            except Exception as e:
                logger.warning(f"读取断点文件失败: {e}，从头开始")
        
        # 过滤未处理的案例
        cases_to_process = []
        for _, case in cases_df.iterrows():
            case_key = f"{case['code']}_{case['date']}"
            if case_key not in processed_codes:
                cases_to_process.append(case.to_dict())
        
        if not cases_to_process:
            print("✅ 所有案例已处理完成！")
            df = pd.DataFrame(existing_results)
            return df
        
        print(f"待处理案例: {len(cases_to_process)} 个")
        
        # 准备任务参数
        tasks = [(case, lookback_weeks, lookback_days, checkpoint_file) for case in cases_to_process]
        
        results = []
        checkpoint_interval = 10  # 每10个结果保存一次
        
        # 优化流程：如果启用GPU批量计算，使用三阶段流程
        if self.use_gpu and self.gpu_calculator:
            # === 阶段1: 并行提取价格数据（网络IO） ===
            if self.verbose:
                print(f"\n【阶段1】并行提取价格数据...")
            
            price_data_cache = {}  # {case_key: prices_df}
            
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                future_to_case = {executor.submit(_extract_price_data_only, task): task[0] 
                                 for task in tasks}
                
                with tqdm(total=len(tasks), desc="提取价格数据", 
                         initial=len(existing_results)) as pbar:
                    for future in as_completed(future_to_case):
                        try:
                            case_key, prices_df = future.result()
                            if prices_df is not None:
                                price_data_cache[case_key] = prices_df
                        except Exception as e:
                            case_dict = future_to_case[future]
                            logger.warning(f"提取价格数据失败 {case_dict.get('code', 'unknown')}: {e}")
                        pbar.update(1)
            
            # === 阶段2: 批量GPU计算技术指标 ===
            if price_data_cache:
                if self.verbose:
                    print(f"\n【阶段2】批量GPU计算技术指标...")
                    print(f"   待处理: {len(price_data_cache)} 个案例")
                
                # 按任务顺序组织价格数据
                prices_list = []
                case_keys = []
                for case in cases_to_process:
                    case_key = f"{case['code']}_{case['date']}"
                    if case_key in price_data_cache:
                        prices_list.append(price_data_cache[case_key])
                        case_keys.append(case_key)
                
                # 批量计算技术指标
                if prices_list:
                    tech_indicators_list = self.gpu_calculator.calculate_batch(prices_list)
                    
                    # 创建技术指标映射
                    tech_indicators_map = {case_keys[i]: tech_indicators_list[i] 
                                          for i in range(len(case_keys))}
                else:
                    tech_indicators_map = {}
                
                if self.verbose:
                    print(f"   ✅ GPU批量计算完成: {len(tech_indicators_map)} 个案例")
            else:
                tech_indicators_map = {}
            
            # === 阶段3: 并行提取其他因子并合并技术指标 ===
            if self.verbose:
                print(f"\n【阶段3】提取完整因子（合并技术指标）...")
            
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                future_to_case = {
                    executor.submit(
                        _extract_factors_with_cached_tech, 
                        task,
                        tech_indicators_map.get(f"{task[0]['code']}_{task[0]['date']}", {})
                    ): task[0] 
                    for task in tasks
                }
                
                with tqdm(total=len(tasks), desc="提取完整因子", 
                         initial=len(existing_results)) as pbar:
                    for future in as_completed(future_to_case):
                        try:
                            result = future.result()
                            if result:
                                results.append(result)
                                existing_results.append(result)
                                
                                # 定期保存断点
                                if len(results) % checkpoint_interval == 0:
                                    try:
                                        df_checkpoint = pd.DataFrame(existing_results)
                                        df_checkpoint.to_csv(checkpoint_file, index=False, encoding='utf-8-sig')
                                        logger.debug(f"已保存断点: {len(existing_results)} 个案例")
                                    except Exception as e:
                                        logger.warning(f"保存断点失败: {e}")
                            
                            pbar.update(1)
                        except Exception as e:
                            case_dict = future_to_case[future]
                            logger.warning(f"处理失败 {case_dict.get('code', 'unknown')}: {e}")
                            pbar.update(1)
        else:
            # === 降级方案：单线程逐个提取（原逻辑） ===
            if self.verbose:
                print(f"\n【并行提取因子】（单线程模式，无GPU批量加速）...")
            
            with ThreadPoolExecutor(max_workers=self.num_workers) as executor:
                future_to_case = {executor.submit(_extract_single_case, task): task[0] 
                                 for task in tasks}
                
                with tqdm(total=len(tasks), desc="并行提取因子", 
                         initial=len(existing_results)) as pbar:
                    for future in as_completed(future_to_case):
                        try:
                            result = future.result()
                            if result:
                                results.append(result)
                                existing_results.append(result)
                                
                                # 定期保存断点
                                if len(results) % checkpoint_interval == 0:
                                    try:
                                        df_checkpoint = pd.DataFrame(existing_results)
                                        df_checkpoint.to_csv(checkpoint_file, index=False, encoding='utf-8-sig')
                                        logger.debug(f"已保存断点: {len(existing_results)} 个案例")
                                    except Exception as e:
                                        logger.warning(f"保存断点失败: {e}")
                            
                            pbar.update(1)
                        except Exception as e:
                            case_dict = future_to_case[future]
                            logger.warning(f"处理失败 {case_dict.get('code', 'unknown')}: {e}")
                            pbar.update(1)
        
        # 合并结果
        all_results = existing_results + results
        
        # 转换为DataFrame
        df = pd.DataFrame(all_results)
        
        # 保存最终结果
        if len(df) > 0:
            try:
                df.to_csv(checkpoint_file, index=False, encoding='utf-8-sig')
                logger.info(f"断点文件已保存: {checkpoint_file}")
            except Exception as e:
                logger.warning(f"保存断点文件失败: {e}")
        
        print(f"\n提取完成: {len(df)} 条预测特征")
        print(f"高收益案例: {(df['is_high_return']).sum()} 条")
        
        return df


def main():
    """测试并行提取"""
    import argparse
    
    parser = argparse.ArgumentParser(description="并行+GPU加速提取预测因子")
    parser.add_argument('--cases-file', type=str, 
                       default='results/high_return_cases_full_train.csv',
                       help='历史案例文件路径')
    parser.add_argument('--output', type=str,
                       default='results/predictive_features_parallel.csv',
                       help='输出文件路径')
    parser.add_argument('--use-gpu', action='store_true', default=True,
                       help='使用GPU加速')
    parser.add_argument('--batch-size', type=int, default=50,
                       help='GPU批处理大小')
    parser.add_argument('--num-workers', type=int, default=3,
                       help='并行线程数')
    
    args = parser.parse_args()
    
    extractor = ParallelPredictorFactorExtractor(
        num_workers=args.num_workers,
        use_gpu=args.use_gpu,
        batch_size=args.batch_size,
        verbose=True
    )
    
    df = extractor.extract_from_historical_cases(
        cases_file=args.cases_file,
        lookback_weeks=1,
        resume=True
    )
    
    df.to_csv(args.output, index=False, encoding='utf-8-sig')
    print(f"\n✅ 预测因子已保存: {args.output}")


if __name__ == '__main__':
    main()
