"""
市场数据验证和填充模块

用于验证和填充缺失的市场数据，确保回测基于准确的数据。
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


def validate_market_data(
    date_str: str,
    limit_up_count: int,
    zhaban_rate: float,
    max_height: int
) -> Dict:
    """
    验证市场数据是否真实
    
    判断逻辑：
    1. 如果涨停家数为0，可能是数据源问题或真实市场状态
    2. 需要结合其他指标判断（如炸板率、连板高度）
    
    Args:
        date_str: 日期字符串
        limit_up_count: 涨停家数
        zhaban_rate: 炸板率（百分比）
        max_height: 最高连板高度
    
    Returns:
        {
            'is_valid': bool,  # 数据是否有效
            'is_data_source_issue': bool,  # 是否是数据源问题
            'confidence': float,  # 置信度（0-1）
            'suggested_values': Dict  # 建议的填充值（如果需要）
        }
    """
    # 如果涨停家数为0，需要验证
    if limit_up_count == 0:
        # 判断是否是数据源问题
        # 如果炸板率和连板高度也为0，很可能是数据源问题
        if zhaban_rate == 0 and max_height == 0:
            return {
                'is_valid': False,
                'is_data_source_issue': True,
                'confidence': 0.8,
                'suggested_values': {}
            }
        # 如果炸板率很高（>50%），可能是真实的市场退潮期
        elif zhaban_rate > 50:
            return {
                'is_valid': True,  # 可能是真实的市场状态
                'is_data_source_issue': False,
                'confidence': 0.6,
                'suggested_values': {
                    'limit_up_count': 0,  # 保持为0
                    'zhaban_rate': zhaban_rate,
                    'max_height': max_height
                }
            }
        else:
            # 其他情况，可能是数据源问题
            return {
                'is_valid': False,
                'is_data_source_issue': True,
                'confidence': 0.7,
                'suggested_values': {}
            }
    
    # 数据有效
    return {
        'is_valid': True,
        'is_data_source_issue': False,
        'confidence': 1.0,
        'suggested_values': {}
    }


def fill_missing_data(
    market_data: Dict[str, Dict],
    history_window: int = 10,
    use_conservative: bool = True
) -> Dict[str, Dict]:
    """
    填充缺失的市场数据
    
    填充策略：
    1. 计算历史有效数据的平均值
    2. 对于数据源问题，使用历史平均值填充
    3. 对于真实市场状态，使用保守估计值填充
    
    Args:
        market_data: 市场数据字典 {date: {limit_up_count, zhaban_rate, max_height}}
        history_window: 历史窗口大小（用于计算平均值）
        use_conservative: 是否使用保守估计（True=保守，False=使用平均值）
    
    Returns:
        填充后的市场数据，包含'is_filled'标记
    """
    # 1. 计算历史有效数据的统计值
    valid_data = [d for d in market_data.values() if d.get('limit_up_count', 0) > 0]
    
    if not valid_data:
        # 如果没有有效数据，使用默认值
        logger.warning("没有有效数据，使用默认值填充")
        avg_limit_up = 50
        avg_zhaban_rate = 25
        avg_max_height = 5
    else:
        # 计算平均值
        avg_limit_up = sum(d.get('limit_up_count', 0) for d in valid_data) / len(valid_data)
        avg_zhaban_rate = sum(d.get('zhaban_rate', 0) for d in valid_data) / len(valid_data)
        avg_max_height = sum(d.get('max_height', 0) for d in valid_data) / len(valid_data)
    
    # 2. 填充缺失数据
    filled_data = {}
    filled_count = 0
    
    for date_str, data in market_data.items():
        limit_up_count = data.get('limit_up_count', 0)
        
        if limit_up_count == 0:
            # 验证数据
            validation = validate_market_data(
                date_str,
                limit_up_count,
                data.get('zhaban_rate', 0),
                data.get('max_height', 0)
            )
            
            if validation['is_data_source_issue']:
                # 数据源问题，使用历史平均值填充
                if use_conservative:
                    # 保守估计：使用平均值的80%
                    filled_limit_up = max(int(avg_limit_up * 0.8), 25)
                    filled_zhaban = avg_zhaban_rate
                    filled_height = max(int(avg_max_height * 0.8), 3)
                else:
                    # 使用平均值
                    filled_limit_up = int(avg_limit_up)
                    filled_zhaban = avg_zhaban_rate
                    filled_height = int(avg_max_height)
                
                filled_data[date_str] = {
                    **data,
                    'limit_up_count': filled_limit_up,
                    'zhaban_rate': filled_zhaban,
                    'max_height': filled_height,
                    'is_filled': True,
                    'fill_reason': 'data_source_issue',
                    'fill_confidence': validation['confidence']
                }
                filled_count += 1
            elif not validation['is_valid']:
                # 其他无效数据，使用保守估计
                filled_limit_up = max(int(avg_limit_up * 0.7), 20)
                filled_zhaban = min(avg_zhaban_rate * 1.2, 50)  # 炸板率可能更高
                filled_height = max(int(avg_max_height * 0.7), 2)
                
                filled_data[date_str] = {
                    **data,
                    'limit_up_count': filled_limit_up,
                    'zhaban_rate': filled_zhaban,
                    'max_height': filled_height,
                    'is_filled': True,
                    'fill_reason': 'invalid_data',
                    'fill_confidence': validation['confidence']
                }
                filled_count += 1
            else:
                # 真实市场状态，保持原值
                filled_data[date_str] = {
                    **data,
                    'is_filled': False
                }
        else:
            # 数据有效，保持原值
            filled_data[date_str] = {
                **data,
                'is_filled': False
            }
    
    logger.info(f"数据填充完成：填充了 {filled_count} 天的缺失数据")
    
    return filled_data


def get_data_quality_stats(market_data: Dict[str, Dict]) -> Dict:
    """
    获取数据质量统计信息
    
    Args:
        market_data: 市场数据字典
    
    Returns:
        {
            'total_days': int,  # 总天数
            'valid_days': int,  # 有效数据天数
            'invalid_days': int,  # 无效数据天数
            'filled_days': int,  # 填充数据天数
            'valid_ratio': float,  # 有效数据比例
            'filled_ratio': float  # 填充数据比例
        }
    """
    total_days = len(market_data)
    valid_days = sum(1 for d in market_data.values() if d.get('limit_up_count', 0) > 0)
    invalid_days = total_days - valid_days
    filled_days = sum(1 for d in market_data.values() if d.get('is_filled', False))
    
    return {
        'total_days': total_days,
        'valid_days': valid_days,
        'invalid_days': invalid_days,
        'filled_days': filled_days,
        'valid_ratio': valid_days / total_days if total_days > 0 else 0,
        'filled_ratio': filled_days / total_days if total_days > 0 else 0
    }
