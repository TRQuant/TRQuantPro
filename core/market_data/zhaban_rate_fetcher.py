"""
炸板率历史数据获取工具

功能：
1. 支持获取指定日期的炸板率数据
2. 支持批量获取历史日期范围的炸板率
3. 自动处理数据缺失和降级方案
4. 支持数据缓存，避免重复请求
5. 回测场景优化

注意：
- AKShare的stock_zt_pool_zbgc_em接口只能获取"近期"的历史数据
- 对于更早的历史数据，需要使用降级方案（估算或从其他数据源推算）
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import time
import logging

logger = logging.getLogger(__name__)


class ZhabanRateFetcher:
    """炸板率数据获取器"""
    
    def __init__(self, cache_enabled: bool = True):
        """
        初始化
        
        Args:
            cache_enabled: 是否启用缓存
        """
        self.cache_enabled = cache_enabled
        self._cache: Dict[str, Dict] = {}  # {date: {zhaban_count, limit_up_count, zhaban_rate}}
        self._ak = None
        
    def _get_akshare(self):
        """延迟加载AKShare"""
        if self._ak is None:
            try:
                import akshare as ak
                self._ak = ak
            except ImportError:
                logger.error("AKShare未安装")
                raise
        return self._ak
    
    def get_zhaban_rate(self, date: str, limit_up_count: Optional[int] = None, validate_date: bool = True) -> Dict:
        """
        获取指定日期的炸板率
        
        Args:
            date: 日期，格式 'YYYYMMDD' 或 'YYYY-MM-DD'
            limit_up_count: 涨停家数（如果已知，可提高准确性）
            
        Returns:
            {
                'date': 日期,
                'zhaban_count': 炸板数量,
                'limit_up_count': 涨停家数,
                'zhaban_rate': 炸板率(%),
                'total_attempts': 总尝试数,
                'source': 数据来源 ('akshare'/'estimated'/'fallback'),
                'success': 是否成功
            }
        """
        # 标准化日期格式
        if '-' in date:
            date_compact = date.replace('-', '')
        else:
            date_compact = date
        
        # 验证日期格式（如果启用）
        if validate_date:
            try:
                datetime.strptime(date_compact, '%Y%m%d')
            except ValueError:
                result = {
                    'date': date_compact,
                    'zhaban_count': 0,
                    'limit_up_count': limit_up_count or 0,
                    'zhaban_rate': 0.0,
                    'total_attempts': 0,
                    'source': 'failed',
                    'success': False,
                    'error': 'Invalid date format'
                }
                return result
        
        # 检查缓存
        if self.cache_enabled and date_compact in self._cache:
            cached = self._cache[date_compact].copy()
            cached['source'] = 'cache'
            return cached
        
        result = {
            'date': date_compact,
            'zhaban_count': 0,
            'limit_up_count': limit_up_count or 0,
            'zhaban_rate': 0.0,
            'total_attempts': 0,
            'source': 'unknown',
            'success': False
        }
        
        # 方法1: 使用AKShare炸板过程接口
        try:
            ak = self._get_akshare()
            zhaban_data = ak.stock_zt_pool_zbgc_em(date=date_compact)
            
            if zhaban_data is not None and not zhaban_data.empty:
                zhaban_count = len(zhaban_data)
                
                # 如果没有提供涨停家数，尝试获取
                if limit_up_count is None:
                    try:
                        limit_up_data = ak.stock_zt_pool_em(date=date_compact)
                        if limit_up_data is not None and not limit_up_data.empty:
                            limit_up_count = len(limit_up_data)
                    except:
                        pass
                
                if limit_up_count and limit_up_count > 0:
                    total_attempts = limit_up_count + zhaban_count
                    zhaban_rate = (zhaban_count / total_attempts * 100) if total_attempts > 0 else 0
                    
                    result.update({
                        'zhaban_count': zhaban_count,
                        'limit_up_count': limit_up_count,
                        'zhaban_rate': zhaban_rate,
                        'total_attempts': total_attempts,
                        'source': 'akshare',
                        'success': True
                    })
                    
                    # 缓存结果
                    if self.cache_enabled:
                        self._cache[date_compact] = result.copy()
                    
                    return result
                    
        except Exception as e:
            logger.debug(f"AKShare炸板过程接口失败 ({date_compact}): {e}")
        
        # 方法2: 降级方案 - 使用实时行情筛选（仅当日有效）
        try:
            # 检查是否是当日
            today_compact = datetime.now().strftime('%Y%m%d')
            if date_compact == today_compact:
                ak = self._get_akshare()
                all_stocks = ak.stock_zh_a_spot_em()
                
                if all_stocks is not None and not all_stocks.empty:
                    # 获取涨停池
                    try:
                        limit_up_data = ak.stock_zt_pool_em(date=date_compact)
                        if limit_up_data is not None and not limit_up_data.empty:
                            limit_up_count = len(limit_up_data)
                            limit_up_codes = set(limit_up_data['代码'].astype(str).values)
                            
                            # 筛选炸板股票（涨跌幅9%-9.5%）
                            all_stocks['代码'] = all_stocks['代码'].astype(str)
                            zhaban_stocks = all_stocks[
                                (all_stocks['涨跌幅'] >= 9.0) & 
                                (all_stocks['涨跌幅'] < 9.5) & 
                                (~all_stocks['代码'].isin(limit_up_codes))
                            ]
                            
                            zhaban_count = len(zhaban_stocks)
                            total_attempts = limit_up_count + zhaban_count
                            zhaban_rate = (zhaban_count / total_attempts * 100) if total_attempts > 0 else 0
                            
                            result.update({
                                'zhaban_count': zhaban_count,
                                'limit_up_count': limit_up_count,
                                'zhaban_rate': zhaban_rate,
                                'total_attempts': total_attempts,
                                'source': 'fallback',
                                'success': True
                            })
                            
                            if self.cache_enabled:
                                self._cache[date_compact] = result.copy()
                            
                            return result
                    except:
                        pass
        except Exception as e:
            logger.debug(f"降级方案失败 ({date_compact}): {e}")
        
        # 方法3: 使用历史平均值估算
        if limit_up_count and limit_up_count > 0:
            # 根据市场经验，炸板率通常在10-20%之间
            # 使用15%作为默认值
            estimated_ratio = 0.15
            zhaban_count = max(1, int(limit_up_count * estimated_ratio))
            total_attempts = limit_up_count + zhaban_count
            zhaban_rate = (zhaban_count / total_attempts * 100) if total_attempts > 0 else 0
            
            result.update({
                'zhaban_count': zhaban_count,
                'limit_up_count': limit_up_count,
                'zhaban_rate': zhaban_rate,
                'total_attempts': total_attempts,
                'source': 'estimated',
                'success': True
            })
            
            logger.warning(f"使用估算值计算炸板率 ({date_compact}): {zhaban_rate:.2f}%")
            
            if self.cache_enabled:
                self._cache[date_compact] = result.copy()
            
            return result
        
        # 完全失败
        result['source'] = 'failed'
        return result
    
    def get_historical_zhaban_rates(
        self, 
        start_date: str, 
        end_date: str,
        limit_up_counts: Optional[Dict[str, int]] = None,
        max_retries: int = 3,
        delay_between_requests: float = 0.5
    ) -> pd.DataFrame:
        """
        批量获取历史炸板率数据
        
        Args:
            start_date: 开始日期 'YYYY-MM-DD' 或 'YYYYMMDD'
            end_date: 结束日期 'YYYY-MM-DD' 或 'YYYYMMDD'
            limit_up_counts: 可选的涨停家数字典 {date: count}
            max_retries: 每个日期最大重试次数
            delay_between_requests: 请求间隔（秒），避免频率限制
            
        Returns:
            DataFrame with columns: date, zhaban_count, limit_up_count, zhaban_rate, total_attempts, source
        """
        # 标准化日期格式
        if '-' in start_date:
            start_compact = start_date.replace('-', '')
        else:
            start_compact = start_date
            
        if '-' in end_date:
            end_compact = end_date.replace('-', '')
        else:
            end_compact = end_date
        
        # 生成交易日列表（简化版，实际应该使用JQData获取交易日）
        start_dt = datetime.strptime(start_compact, '%Y%m%d')
        end_dt = datetime.strptime(end_compact, '%Y%m%d')
        
        dates = []
        current = start_dt
        while current <= end_dt:
            # 简单过滤：排除周末（更准确的应该使用交易日历）
            if current.weekday() < 5:  # 0-4 = 周一到周五
                dates.append(current.strftime('%Y%m%d'))
            current += timedelta(days=1)
        
        results = []
        total = len(dates)
        
        logger.info(f"开始批量获取炸板率数据: {start_compact} ~ {end_compact} ({total}个日期)")
        
        for idx, date_compact in enumerate(dates, 1):
            limit_up_count = limit_up_counts.get(date_compact) if limit_up_counts else None
            
            # 重试逻辑
            for attempt in range(max_retries):
                try:
                    result = self.get_zhaban_rate(date_compact, limit_up_count)
                    results.append(result)
                    
                    if idx % 10 == 0 or idx == total:
                        logger.info(f"进度: {idx}/{total} ({idx/total*100:.1f}%)")
                    
                    # 请求间隔
                    if idx < total and delay_between_requests > 0:
                        time.sleep(delay_between_requests)
                    
                    break
                except Exception as e:
                    if attempt == max_retries - 1:
                        logger.warning(f"获取 {date_compact} 失败（已重试{max_retries}次）: {e}")
                        # 使用估算值
                        if limit_up_count and limit_up_count > 0:
                            estimated_ratio = 0.15
                            zhaban_count = max(1, int(limit_up_count * estimated_ratio))
                            total_attempts = limit_up_count + zhaban_count
                            zhaban_rate = (zhaban_count / total_attempts * 100) if total_attempts > 0 else 0
                            
                            results.append({
                                'date': date_compact,
                                'zhaban_count': zhaban_count,
                                'limit_up_count': limit_up_count,
                                'zhaban_rate': zhaban_rate,
                                'total_attempts': total_attempts,
                                'source': 'estimated',
                                'success': True
                            })
                    else:
                        time.sleep(1)  # 重试前等待
        
        df = pd.DataFrame(results)
        
        if not df.empty:
            # 添加日期列（标准格式）
            df['date_std'] = pd.to_datetime(df['date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
            # 按日期排序
            df = df.sort_values('date').reset_index(drop=True)
            
            # 统计信息
            success_count = df['success'].sum()
            source_counts = df['source'].value_counts()
            
            logger.info(f"完成！成功: {success_count}/{total}, 数据来源: {dict(source_counts)}")
        
        return df
    
    def clear_cache(self):
        """清空缓存"""
        self._cache.clear()
        logger.info("缓存已清空")


# 便捷函数
def get_zhaban_rate(date: str, limit_up_count: Optional[int] = None) -> Dict:
    """
    获取指定日期的炸板率（便捷函数）
    
    Args:
        date: 日期 'YYYYMMDD' 或 'YYYY-MM-DD'
        limit_up_count: 涨停家数（可选）
        
    Returns:
        炸板率数据字典
    """
    fetcher = ZhabanRateFetcher()
    return fetcher.get_zhaban_rate(date, limit_up_count)


def get_historical_zhaban_rates(
    start_date: str,
    end_date: str,
    limit_up_counts: Optional[Dict[str, int]] = None,
    max_retries: int = 3,
    delay_between_requests: float = 0.5
) -> pd.DataFrame:
    """
    批量获取历史炸板率（便捷函数）
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        limit_up_counts: 涨停家数字典（可选）
        
    Returns:
        DataFrame
    """
    fetcher = ZhabanRateFetcher()
    return fetcher.get_historical_zhaban_rates(start_date, end_date, limit_up_counts)
