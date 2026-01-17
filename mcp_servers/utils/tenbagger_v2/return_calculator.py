"""
收益率计算工具

参考: docs/TENBAGGER_REPORT_ENHANCED.html
"""

from typing import Optional, Dict
from datetime import datetime


def calculate_return_rate(
    analysis_price: float,
    current_price: float,
    research_end_price: Optional[float] = None,
    analysis_date: Optional[str] = None,
    current_date: Optional[str] = None,
    research_end_date: Optional[str] = None
) -> Dict[str, any]:
    """
    计算收益率（参考TENBAGGER_REPORT_ENHANCED.html）
    
    Args:
        analysis_price: 识别价（分析时价格）
        current_price: 当前价
        research_end_price: 研究期末价（可选）
        analysis_date: 识别日期（可选，格式：YYYY-MM-DD）
        current_date: 当前日期（可选，格式：YYYY-MM-DD）
        research_end_date: 研究期末日期（可选，格式：YYYY-MM-DD）
    
    Returns:
        dict: 包含总收益率、研究期后收益率等信息
    """
    # 总收益率 = (当前价 - 识别价) / 识别价 × 100%
    total_return = 0.0
    if analysis_price > 0:
        total_return = (current_price - analysis_price) / analysis_price * 100
    
    # 研究期后收益率 = (当前价 - 研究期末价) / 研究期末价 × 100%
    post_research_return = None
    if research_end_price and research_end_price > 0:
        post_research_return = (current_price - research_end_price) / research_end_price * 100
    
    result = {
        'total_return': round(total_return, 2),
        'analysis_price': analysis_price,
        'current_price': current_price,
    }
    
    if post_research_return is not None:
        result['post_research_return'] = round(post_research_return, 2)
        result['research_end_price'] = research_end_price
    
    if analysis_date:
        result['analysis_date'] = analysis_date
    if current_date:
        result['current_date'] = current_date
    if research_end_date:
        result['research_end_date'] = research_end_date
    
    return result


def format_return_rate(return_rate: float, show_sign: bool = True) -> str:
    """
    格式化收益率显示
    
    Args:
        return_rate: 收益率（百分比）
        show_sign: 是否显示正负号
    
    Returns:
        格式化后的字符串，如 "+21.21%" 或 "-7.63%"
    """
    if return_rate > 0:
        return f"+{return_rate:.2f}%"
    elif return_rate < 0:
        return f"{return_rate:.2f}%"
    else:
        return "0.00%"


def get_return_rate_class(return_rate: float) -> str:
    """
    获取收益率对应的CSS类名
    
    Args:
        return_rate: 收益率（百分比）
    
    Returns:
        CSS类名：'positive' 或 'negative'
    """
    return 'positive' if return_rate > 0 else 'negative'

