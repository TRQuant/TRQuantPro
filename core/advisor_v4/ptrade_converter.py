#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ptrade策略转换器 - 将BulletTrade/聚宽策略转换为Ptrade代码

Ptrade特点:
- 恒生电子提供的量化交易平台
- API与聚宽类似但有差异
- 使用.SH/.SZ股票代码格式

主要转换:
1. 股票代码格式
2. 数据获取API (get_price → get_klines)
3. 订单API参数差异
4. 持仓查询API差异
5. 定时任务 (run_daily → schedule)
"""

from __future__ import annotations

import logging
import re
from typing import Dict

from .strategy_converter import StrategyConverter, ConversionResult

logger = logging.getLogger(__name__)


class PtradeConverter(StrategyConverter):
    """BulletTrade/聚宽 → Ptrade 策略转换器"""
    
    # 函数名映射
    FUNCTION_MAPPING = {
        'get_price': 'get_klines',
        'get_index_stocks': 'get_index_component',
        'get_all_securities': 'get_stock_list',
        'order_target': 'order_to',
        'before_trading_start': 'before_market_open',
        'after_trading_end': 'after_market_close',
    }
    
    # 属性映射
    ATTRIBUTE_MAPPING = {
        'total_value': 'market_value',
        'total_amount': 'total_qty',
        'closeable_amount': 'enable_qty',
        'avg_cost': 'cost_price',
    }
    
    @property
    def target_platform(self) -> str:
        return "Ptrade"
    
    @property
    def source_platform(self) -> str:
        return "BulletTrade/聚宽"
    
    def _convert_imports(self, code: str) -> str:
        """转换导入语句"""
        result = code
        
        # 移除聚宽特有的导入
        jq_imports = [
            r'from jqdata import \*',
            r'import jqdatasdk.*',
            r'from jqdatasdk import.*',
        ]
        for pattern in jq_imports:
            if re.search(pattern, result):
                self.converted_items['imports'] += 1
                result = re.sub(pattern, '# ' + pattern.replace(r'\*', '*'), result)
                self._add_warning(f"注释掉聚宽导入: {pattern}")
        
        return result
    
    def _convert_function_calls(self, code: str) -> str:
        """转换函数调用（增强版，处理参数差异）"""
        result = super()._convert_function_calls(code)
        
        # 特殊处理: get_price → get_klines 参数转换
        # get_price(security, start_date, end_date, frequency, fields)
        # get_klines(security, count, frequency)
        if 'get_klines' in result:
            self._add_warning("get_klines参数与get_price不同，需要手动调整")
        
        # 特殊处理: order_value 在Ptrade中不直接支持
        if 'order_value' in result:
            self._add_warning("Ptrade不支持order_value，需要手动转换为order")
        
        # 特殊处理: order_target_value 在Ptrade中不直接支持
        if 'order_target_value' in result:
            self._add_warning("Ptrade不支持order_target_value，需要手动转换")
        
        return result
    
    def _add_platform_specific_code(self, code: str) -> str:
        """添加Ptrade平台特定代码"""
        
        # 添加Ptrade头部注释
        header = '''# -*- coding: utf-8 -*-
"""
策略已转换为Ptrade平台格式
原始平台: BulletTrade/聚宽
转换时间: 自动生成

注意事项:
1. 请检查股票代码格式已转换为.SH/.SZ
2. get_klines参数与get_price不同，需调整
3. 定时任务需要使用Ptrade的schedule语法
4. order_value/order_target_value需要手动转换
"""

'''
        # 添加Ptrade导入
        ptrade_imports = '''
# Ptrade平台导入
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Ptrade API（实际运行时由平台提供）
# from ptrade import *

'''
        
        # 检查是否已有头部
        if code.strip().startswith('#'):
            # 已有注释头，在第一个函数定义前插入导入
            result = header + code
        else:
            result = header + ptrade_imports + code
        
        return result
    
    def _post_process(self, code: str) -> str:
        """后处理"""
        result = code
        
        # 转换定时任务语法
        # run_daily(func, time='09:30') → schedule(time='09:30', func=func)
        run_daily_pattern = r"run_daily\s*\(\s*(\w+)\s*,\s*time\s*=\s*['\"](\d+:\d+)['\"]\s*\)"
        matches = re.findall(run_daily_pattern, result)
        for func_name, time_str in matches:
            old = f"run_daily({func_name}, time='{time_str}')"
            new = f"schedule(time='{time_str}', func={func_name})"
            result = result.replace(old, new)
            self._add_warning(f"定时任务转换: {old} → {new}")
        
        # 转换run_weekly
        run_weekly_pattern = r"run_weekly\s*\(\s*(\w+)\s*,\s*weekday\s*=\s*(\d+)\s*,\s*time\s*=\s*['\"](\d+:\d+)['\"]\s*\)"
        matches = re.findall(run_weekly_pattern, result)
        for func_name, weekday, time_str in matches:
            old = f"run_weekly({func_name}, weekday={weekday}, time='{time_str}')"
            # Ptrade使用crontab格式: 分 时 日 月 周
            hour, minute = time_str.split(':')
            new = f"schedule('{minute} {hour} * * {int(weekday)+1}', func={func_name})"
            result = result.replace(old, new)
            self._add_warning(f"定时任务转换: {old} → {new}")
        
        return result


def convert_to_ptrade(source_code: str, verbose: bool = True) -> ConversionResult:
    """
    便捷函数：将BulletTrade/聚宽策略转换为Ptrade格式
    
    Args:
        source_code: 源策略代码
        verbose: 是否输出详细信息
        
    Returns:
        转换结果
    """
    converter = PtradeConverter(verbose=verbose)
    return converter.convert(source_code)


# 测试代码
if __name__ == '__main__':
    # 测试代码
    test_code = '''
from jqdata import *

def initialize(context):
    g.stock_pool = get_index_stocks('000300.XSHG')
    run_daily(check_stocks, time='09:30')

def check_stocks(context):
    prices = get_price('000001.XSHE', start_date='2024-01-01', end_date='2024-01-31')
    if context.portfolio.positions['000001.XSHE'].total_value > 10000:
        order('000001.XSHE', -100)
'''
    
    result = convert_to_ptrade(test_code)
    print("=" * 60)
    print(f"转换成功: {result.success}")
    print(f"警告数: {len(result.warnings)}")
    print(f"错误数: {len(result.errors)}")
    print(f"转换统计: {result.converted_items}")
    print("=" * 60)
    print(result.target_code)
