"""
工具函数模块

提供股票代码转换、数据获取等辅助功能。
"""

from typing import Tuple, Optional


def identify_exchange_and_convert(code: str) -> Tuple[Optional[str], str, bool]:
    """
    识别股票交易所类型并转换为JQData格式
    
    Args:
        code: 股票代码（6位数字字符串）
    
    Returns:
        (jq_code, exchange_type, is_valid)
        - jq_code: JQData格式代码（如果支持），否则为None
        - exchange_type: 交易所类型（'XSHE'/'XSHG'/'BSE'/'OTHER'）
        - is_valid: 是否可以在JQData中查询
    """
    if not code:
        return None, 'OTHER', False
    
    code_str = str(code)
    if len(code_str) != 6:
        return None, 'OTHER', False
    
    # 北交所股票（92开头）
    if code_str.startswith('92'):
        return None, 'BSE', False  # 北交所，JQData不支持
    
    # 深市股票（00、30开头）
    if code_str.startswith('00') or code_str.startswith('30'):
        return f"{code_str}.XSHE", 'XSHE', True
    
    # 沪市股票（60、68开头）
    elif code_str.startswith('60') or code_str.startswith('68'):
        return f"{code_str}.XSHG", 'XSHG', True
    
    # 其他格式
    return None, 'OTHER', False


def convert_code_to_jq(code: str) -> Optional[str]:
    """
    将AKShare股票代码转换为JQData格式（兼容旧接口）
    
    Args:
        code: 股票代码（6位数字字符串）
    
    Returns:
        JQData格式代码，如果不支持则返回None
    """
    jq_code, _, is_valid = identify_exchange_and_convert(code)
    return jq_code if is_valid else None
